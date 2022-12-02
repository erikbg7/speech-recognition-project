import socket

HOST = "127.0.0.1"
PORT = 65432

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((HOST, PORT))
client_sock.sendall(b"Message from client")
res = client_sock.recv(1024)

print("Client", res)
