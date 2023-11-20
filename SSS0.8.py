from tkinter import messagebox
import requests
import csv
from tkinter import *
from tkinter import filedialog 
import base64
from tkinter import ttk

# Создание окна приложения
window = Tk()
window.title("SSS 0.8")  # Заголовок окна
window.geometry("290x230")  # Размеры окна
window["bg"] = "Silver"  # Цвет фона окна

# Словарь с API Endpoint
API_ENDPOINTS = {
    "BePaid   (APM)": "https://api.bepaid.by/beyag/transactions",
    "Paysage  (APM)": "https://api.paysage.io/beyag/transactions",
    "ConstantPos (APM)": "https://api.constantpos.com/beyag/transactions",
    "Payes    (APM)": "https://api.payes.io/beyag/transactions",
    "BePaid   (Card)": "https://gateway.bepaid.by/transactions",
    "Paysage  (Card)": "https://gateway.paysage.io/transactions",
    "ConstantPos (Card)": "https://gateway.constantpos.com/transactions",
    "Payes    (Card)": "https://gateway.payes.io/transactions"
}

selected_api_endpoint = StringVar()  # Переменная для хранения выбранного значения из выпадающего списка

def save_values():
    """
    Функция сохраняет значения из полей в переменные.
    """
    global USER, PASSWORD, API_ENDPOINT
    USER = entry_shop_id.get()  # Значение из поля "Shop ID"
    PASSWORD = entry_secret_key.get()  # Значение из поля "Secret Key"
    API_ENDPOINT = API_ENDPOINTS[selected_api_endpoint.get()]  # Получить выбранное значение и установить API_ENDPOINT

def check_transactions():
    """
    Функция выполняет проверку транзакций, создает файл output.csv с результатами.
    """
    # Открытие CSV-файла для записи
    with open("output.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["transaction_id", "transaction_status"])

        # Чтение каждого ID из файла ids.txt и выполнение HTTP-запроса
        with open("ids.txt", "r") as idsfile:
            for transaction_id in idsfile:
                transaction_id = transaction_id.strip()
                print(f"Processing transaction ID: {transaction_id}")

                # Выполнение HTTP-запроса
                auth = (USER, PASSWORD)  # Замените USER и PASSWORD на соответствующие значения
                response = requests.get(f"{API_ENDPOINT}/{transaction_id}", auth=auth)
                response_json = response.json()

                # Извлечение статуса транзакции из ответа
                transaction_status = response_json["transaction"]["status"]
                print(f"Transaction status: {transaction_status}")

                # Проверка, если статус транзакции пустой, заменить на "N/A"
                if not transaction_status:
                    transaction_status = "N/A"
                    print("Transaction status is empty. Setting to 'N/A'.")

                # Помещение статуса в отдельную ячейку в отдельном столбце
                transaction_status_cell = f"{transaction_status}"  # Здесь добавлена строка для отдельной ячейки
                writer.writerow([transaction_id, transaction_status_cell])  # Здесь передана новая переменная

                print(f"Processed transaction ID: {transaction_id}")
                print()

    messagebox.showinfo("Success", "Готово!")  # Отображение окна с сообщением о завершении проверки



# Создание и размещение элементов на окне
label_shop_id = Label(window, text="Shop ID:")
label_shop_id.grid(row=0, column=0, padx=10, pady=10)
entry_shop_id = Entry(window)
entry_shop_id.grid(row=0, column=1, padx=10, pady=10)

label_secret_key = Label(window, text="Secret Key:")
label_secret_key.grid(row=1, column=0, padx=10, pady=10)
entry_secret_key = Entry(window)
entry_secret_key.grid(row=1, column=1, padx=10, pady=10)

# Создание выпадающего списка
label_api_endpoint = Label(window, text="API Endpoint:")
label_api_endpoint.grid(row=2, column=0, padx=10, pady=10)
api_endpoint_combobox = ttk.Combobox(window, textvariable=selected_api_endpoint, values=list(API_ENDPOINTS.keys()))
api_endpoint_combobox.grid(row=2, column=1, padx=10, pady=10)

button_save = Button(window, text="login", command=save_values)
button_save.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

button_start = Button(window, text="Start", command=check_transactions)
button_start.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

window.mainloop()