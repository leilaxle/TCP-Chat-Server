import socket
import select
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print("Correct usage: python client.py <server IP address> <server port number>")
    sys.exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
client.connect((IP_address, Port))

while True:
    sockets_list = [sys.stdin, client]

    read_sockets, _, _ = select.select(sockets_list, [], [])

    for sock in read_sockets:
        if sock == client:
            message = sock.recv(2048).decode()
            print(message)
        else:
            message = sys.stdin.readline()
            client.send(message.encode())
