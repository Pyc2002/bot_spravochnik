import csv
import os
import constants
from constants import DATA_BASE





def fieldnames():
    """Create file.csv if it not exists, to avoid duplicate headers
    
    args -> None
    returns -> None
    """
    if not os.path.exists(DATA_BASE): 
        with open(DATA_BASE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, dialect='excel', delimiter='|')
            writer.writerow(['Имя', 'Фамилия', 'Телефон', 'Группа', 'Комментарий'])
            file.close()


def add_contact():
    """ Adding data of new contact in csv-file. User inputs data (str), def create dict and add it in file.
    args -> None
    returns -> None
    """
    fieldnames()
    new_contact = constants.CONTACT_DATA
   
    

    with open(DATA_BASE, mode='a', newline='', encoding='utf-8') as csv_file:
       
        field_names = constants.CONTACT_DATA.keys()

        writer = csv.DictWriter(csv_file, fieldnames=field_names, dialect='excel', restval='', delimiter='|')
        writer.writerow(new_contact)
        csv_file.close()



def Search_contact(update):
    """ Searching contact in csv-file. User inputs data (str), def create string with results.
    args -> None
    returns -> str
    """
    data = update.message.text
    # data = input(' ВВендите имя\n')
    result = ''
   
    with open(DATA_BASE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for item in reader:
            
            if data.title() in item['Имя'] or data.title() in item['Фамилия'] or data.title() in item['Группа']:
                
                res = item['Имя']+ ' ' + item['Фамилия']+ ' ' + item['Телефон']+ ' ' + item['Группа']+ ' ' + item['Комментарий']
                result += res + '\n'
    
        return result
    
            
def Delete_contact(update):
    """ Removing contact in csv-file. User inputs data (str), def create new file without contact, removed old file and renemed new.
    args -> None
    returns -> None
    """
    data = update.message.text
    # data = input(' ВВендите номер\n')
    with open(DATA_BASE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        with open('temp.csv', mode='w', encoding='utf-8', newline='') as temp_file:
            writer = csv.DictWriter(temp_file, fieldnames=reader.fieldnames, dialect='excel', restval='', delimiter='|')
            writer.writeheader()
            writer.writerows(filter(lambda x: x.get('Телефон') not in data, reader))

    os.remove(DATA_BASE)
    os.rename('temp.csv',DATA_BASE)
    
    




