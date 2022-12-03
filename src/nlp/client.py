import socket
import pickle
from factory import Product


HOST = "127.0.0.1"
PORT = 65432


def get_products_from_sentence(sentence: str):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((HOST, PORT))
    client_sock.sendall(pickle.dumps(sentence))
    bytes = client_sock.recv(1024)
    products: list[Product] = pickle.loads(bytes)
    return products
