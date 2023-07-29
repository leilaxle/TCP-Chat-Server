import socket
import select
import sys
import _thread as thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 3:
    print("Correct usage: python server.py <IP address> <port number>")
    sys.exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])  # Use the specified port number

server.bind((IP_address, Port))
server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
    conn.send("Welcome to the chat room!".encode())

    while True:
        try:
            message = conn.recv(2048).decode()
            if message:
                print("<" + addr[0] + "> " + message)
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove(client)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    thread.start_new_thread(clientthread, (conn, addr))
