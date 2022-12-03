# Should recive the document received from the NLP process, and return
# a single or multiple product with the amount and the name

import socket
import pickle
import factory
from spacy import load


HOST = "127.0.0.1"
PORT = 65432

nlp = load("es_core_news_sm")


def process_connection(sock: socket.socket):
    print("Processing client request...")
    data = sock.recv(1024)
    text: str = pickle.loads(data)
    print("Server text --> ", text)
    products = factory.get_products(nlp(text))
    sock.sendall(pickle.dumps(products))
    sock.close()
    print("Finished request, closing socket...")


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen(5)

print("Listening on port {}...".format(PORT))
print("\n")

try:
    while True:
        conn, address = server_sock.accept()
        process_connection(conn)
except KeyboardInterrupt:
    print("\nServer process terminated.")
finally:
    server_sock.close()
