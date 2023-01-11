from constants import LOG_NAME
from datetime import datetime as dt
import csv


def write(data):
    """
    Записывает в лог-файл информацию о добавлении нового контакта

    args -> data (any)
    return -> None
    """
    time = dt.now().strftime("%d-%m-%Y, %H:%M")
    with open (LOG_NAME, 'a', encoding='utf-8') as log_file:
        log_file.write('{}: Добавлен: {}\n'.format(time,data))

def write_del(data):
    """
    Записывает в лог-файл информацию об удалении контакта

    args -> data (any)
    return -> None
    """
    time = dt.now().strftime("%d-%m-%Y, %H:%M")
    with open (LOG_NAME, 'a', encoding='utf-8') as log_file:
        log_file.write('{}: Удален контакт с номером телефона: {}\n'.format(time,data))


def view_log():
    """
    Считывает из лог-файла информацию 

    args -> None
    return -> None
    """
    with open(LOG_NAME, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(', '.join(row))