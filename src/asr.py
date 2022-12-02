import speech_recognition as sr
from client import get_products_from_sentence

r = sr.Recognizer()


class Invoice:
    expenses = []

    def __init__(self, client, month):
        self.client = client
        self.month = month

    def __str__(self):
        return f"Client: {self.client}\nMonth: {self.month}"

    def add_expense(self, expense):
        self.expenses.append(expense)

    def get_expenses(self):
        return self.expenses


listening = True
invoice_opened = False
current_invoice: Invoice = None
months = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


def process_invoice_order(txt: str):
    words = txt.split()
    keyword = words[0]
    month = words[len(words) - 1]
    client = " ".join(words[1 : len(words) - 1])
    return keyword, client, month


def create_invoice(txt: str):
    keyword, client, month = process_invoice_order(txt)
    if keyword != "factura":
        return print("Keyword is not valid")
    if month not in months:
        return print("Month is not valid")
    global current_invoice
    global invoice_opened
    current_invoice = Invoice(client, month)
    invoice_opened = True


def print_products(products):
    print("\n")
    for p in products:
        print(p.__str__())
        print("\n")
    print("\n")


def get_processed_text(txt: str):
    print("requesting products to server...")
    products = get_products_from_sentence(txt)
    print_products(products)


def process_sentence(txt: str):
    lower_txt = txt.lower()
    global invoice_opened
    if invoice_opened == False:
        create_invoice(lower_txt)
    else:
        if lower_txt == "fin factura":
            global listening
            listening = False
        else:
            get_processed_text(lower_txt)
            current_invoice.add_expense(lower_txt)


def print_current_invoice():
    print("\n")
    print(current_invoice.__str__())
    for x in current_invoice.get_expenses():
        print("- ", x)
    print("\n")


while listening:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5

        if invoice_opened:
            print("Next order...")
        else:
            print("watiing for invoice...")

        if invoice_opened and current_invoice:
            print_current_invoice()

        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="es-ES")
            process_sentence(text)
        except sr.UnknownValueError as e:
            print(e)
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Google Speech Recognition service is not reachable {0}".format(e))


print("Programm finished")
