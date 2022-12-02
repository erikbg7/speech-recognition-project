import socket
import pickle
from factory import Product

HOST = "127.0.0.1"
PORT = 65432

test_sentence = "tres barras de quarto diez panes de hamburguesa y un pan de medio"

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((HOST, PORT))
client_sock.sendall(pickle.dumps(test_sentence))

bytes = client_sock.recv(1024)
products: list[Product] = pickle.loads(bytes)

for p in products:
    print(p.__str__())
    print("\n")
