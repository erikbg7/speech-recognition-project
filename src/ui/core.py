import factory
from spacy import load


nlp = load("es_core_news_sm")


def process_request(text: str):
    doc = nlp(text)
    results = factory.get_products(doc)
    return results
