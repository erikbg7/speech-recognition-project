# Should recive the document received from the NLP process, and return
# a single or multiple product with the amount and the name

from spacy import load
from spacy.tokens import Token
from text_to_num import text2num


class Product:
    def __init__(self):
        self.amount = 0
        self.tokens = []

    def set_amount(self, amount):
        self.amount = amount

    def add_token(self, token):
        self.tokens.append(token)

    def __str__(self) -> str:
        return f"amount: {self.amount}, tokens: {self.tokens}"


def is_amount(token):
    return token.pos_ == "NUM" or (
        token.pos_ == "DET"
        and (token.text.lower() == "un" or token.text.lower() == "una")
    )


def get_products(tokens: list[Token]):
    products = []

    product = Product()

    for token in tokens:
        if is_amount(token):

            numeric_amount = text2num(token.text, "es")

            if len(product.tokens) > 0:
                products.append(product)
                product = Product()
                product.set_amount(numeric_amount)
            else:
                product = Product()
                product.set_amount(numeric_amount)

        if token.pos_ == "NOUN" or token.pos_ == "PROPN":
            product.add_token(token)

    if len(product.tokens) > 0:
        products.append(product)

    return products


nlp_sm = load("es_core_news_sm")
doc_sm = nlp_sm("tres barras de quarto diez panes de hamburguesa y un pan de medio")

products = get_products(doc_sm)

for p in products:
    print(p.__str__())
    print("\n")
