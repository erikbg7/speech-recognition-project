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


def is_amount(token: Token):
    pos = token.pos_
    text = token.text.lower()
    return pos == "NUM" or (pos == "DET" and (text == "un" or text == "una"))


def get_products(tokens: list[Token]):
    products: list[Product] = []
    product = Product()

    for token in tokens:
        if is_amount(token):

            if len(product.tokens) > 0:
                products.append(product)

            product = Product()
            amount = text2num(token.text, "es")
            product.set_amount(amount)

        if token.pos_ == "NOUN" or token.pos_ == "PROPN":
            # We should not add the token, we should process it again.
            # A product should only have a product id, not a full token.
            product.add_token(token.text)

    if len(product.tokens) > 0:
        products.append(product)

    return products
