import speech_recognition as sr

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


def create_invoice(txt: str):
    words = txt.split()
    keyword = words[0]
    if keyword == "factura":
        client = " ".join(words[1 : len(words) - 1])
        month = words[len(words) - 1]
        if month in months:
            global current_invoice
            current_invoice = Invoice(client, month)
            global invoice_opened
            invoice_opened = True
        else:
            print("Month is not valid")
    else:
        print("Keyword is not valid")


def add_expense(txt: str):
    current_invoice.add_expense(txt)


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
            add_expense(lower_txt)


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

        print("Next order..." if invoice_opened else "Waiting for invoice...")
        if invoice_opened and current_invoice:
            print_current_invoice()

        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="es-ES")
            process_sentence(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(
                    e
                )
            )


print("Programm finished")
