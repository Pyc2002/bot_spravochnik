import csv
from constants import DATA_BASE

# def Check_none(update):
#     """
#     Testing input data for None

#     args -> str
#     return -> bool
#     """
#     data = update.message.text
#     with open(DATA_BASE, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile, delimiter='|')
#         for item in reader:
#             if data.title() not in item.values(): 
#                 update.message.reply_text('Ошибка! Такого нет в базе \n\n'
#                 'Повторите ввод \n')
#                 return False
#     return True
            
                
    

def Check_num(update):
    """
    Testing input data for digits

    args -> str
    return -> bool
    """  
    data = update.message.text
    if not data.isdigit():
        update.message.reply_text('Ошибка! Принимаются только цифры \n\n'
        'Повторите ввод \n' 'Команда /cancel, чтобы прекратить разговор.')
        return False
    return True
    

    
def Check_name(update):
    """ Testing input data for letters 
    
    args -> str
    return -> bool
    """
    data = update.message.text
    if not data.isalpha():
        update.message.reply_text('Ошибка! Принимаются только буквы \n\n'
        'Повторите ввод \n' 'Команда /cancel, чтобы прекратить разговор.')
        return False
    return True


def Check_phone(update):
    """Testing input numer for overlap
    args -> str
    retuns -> bool
    """
    data = update.message.text
    with open(DATA_BASE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for item in reader:
            if data in item['Телефон']:
                update.message.reply_text('Этот номер телефона уже записан в справочнике \n\n'
                'введите другой номер \n' 'Команда /cancel, чтобы прекратить разговор.')
                return False    
    return True
