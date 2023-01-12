from config import TOKEN
import logging, controller, checks, constants



from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext
    
)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


CHOICE, STEP_NAME, STEP_LAST_NAME, STEP_PHONE_NUM, STEP_GROUP, STEP_COMMENT, SEARCH, DELETE, DELETE_SECOND = range(9)



def start(update, _):
    """ Запускает ConversationHandler и дает выбор действий
    args -> update message
    return -> int (переход на следующий шаг по списку)
    """
 
    reply_keyboard = [['Добавить контакт', 'Найти контакт', 'Удалить контакт']]
    
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
  
    update.message.reply_text(
        'Что вы хотите сделать? '
        'Команда /cancel, чтобы прекратить разговор.\n\n',
        reply_markup=markup_key,)
    return CHOICE

def Choice(update, _):
    """ Записывает поступившее сообщение и запускает следующее сообщение в телеграм в зависимости от сделанного выбора
    args -> update message
    return -> int (переход на следующий шаг по списку)
    """
    if update.message.text == 'Добавить контакт': 
        update.message.reply_text('Введите имя.\n''Команда /cancel, чтобы прекратить разговор.\n\n', reply_markup=ReplyKeyboardRemove(),) 
        return STEP_NAME
    elif update.message.text == 'Найти контакт':
        update.message.reply_text('Введите имя или фамилию или группу.\n''Команда /cancel, чтобы прекратить разговор.\n\n', reply_markup=ReplyKeyboardRemove(),) 
        return SEARCH
    elif update.message.text == 'Удалить контакт': 
        update.message.reply_text('Введите имя или фамилию для удаления\n' 'Команда /cancel, чтобы прекратить разговор.\n\n', reply_markup=ReplyKeyboardRemove(),)
        return DELETE
 

def Name(update, _):
    """ Записывает поступившее сообщение и запускает следующее сообщение в телеграм 
    args -> update message
    return -> int (переход на следующий шаг по списку)
    """
    user = update.message.from_user
    constants.NAME = update.message.text
    if checks.Check_name(update) == False: return STEP_NAME
    logger.info("Пользователь %s добавил имя: %s", user.first_name, update.message.text)
    update.message.reply_text('Введите фамилию.\n' 'Команда /cancel, чтобы прекратить разговор.')
    return STEP_LAST_NAME
    

def Last_name(update, _):
    """ Записывает поступившее сообщение и запускает следующее сообщение в телеграм 
    args -> update message
    return -> int (переход на следующий шаг по списку)
    """
    user = update.message.from_user
    constants.LAST_NAME = update.message.text
    if checks.Check_name(update) == False: return STEP_LAST_NAME
    logger.info("Пользователь %s добавил фамилию: %s", user.first_name, update.message.text)
    update.message.reply_text('Введите номер телефона.\n' 'Команда /cancel, чтобы прекратить разговор.')
    return STEP_PHONE_NUM

def Phone_num(update, _):
    """ Записывает поступившее сообщение и запускает следующее сообщение в телеграм 
    args -> update message
    return -> int (переход на следующий шаг по списку)
    """
    user = update.message.from_user
    if checks.Check_num(update) == False: return STEP_PHONE_NUM
    if checks.Check_phone(update) == False: return STEP_PHONE_NUM
    constants.PHONE_NUM = update.message.text
    logger.info("Пользователь %s добавил номер телефона: %s", user.first_name, update.message.text)
    update.message.reply_text('Введите группу или отправь /skip, если без группы.\n' 'Команда /cancel, чтобы прекратить разговор.')
    return STEP_GROUP

def Group(update, _):
    """ Записывает поступившее сообщение и запускает следующее сообщение в телеграм 
    args -> update message
    return -> int (переход на следующий шаг по списку)
    """
    user = update.message.from_user
    constants.GROUP = update.message.text
    logger.info("Пользователь %s добавил группу: %s", user.first_name, update.message.text)
    update.message.reply_text('Введите комментарий или отправь /skip, если без комментария.\n' 'Команда /cancel, чтобы прекратить разговор.')
    return STEP_COMMENT

def skip_group(update, _):
    """ Записывает поступившее сообщение и пропускает шаг
    args -> update message
    return -> int (переход на следующий шаг по списку)
    """
    user = update.message.from_user
    logger.info("Пользователь %s пропустил заполнение группы.", user.first_name)
    update.message.reply_text('Тогда введите комментарий , если не хотите тогда отправьте /skip\n')
    return STEP_COMMENT

def Comment(update, _):
    """ Записывает поступившее сообщение и завершает разговор
    args -> update message
    return -> завершение ConversationHandler
    """
    user = update.message.from_user
    constants.COMMENT = update.message.text
    logger.info("Пользователь %s добавил Комментарий: %s", user.first_name, update.message.text)
    update.message.reply_text('Данные сохранены!\n' 'Для перехода в меню отправьте /start')
    controller.add_contact()
    return ConversationHandler.END

def skip_comment(update, _):
    """ Записывает поступившее сообщение и пропускает шаг
    args -> update message
    return -> завершение ConversationHandler
    """
    user = update.message.from_user
    logger.info("Пользователь %s пропустил заполнение комментария.", user.first_name)
    update.message.reply_text('Данные сохранены!\n' 'Для перехода в меню отправьте /start')
    controller.add_contact()
    return ConversationHandler.END

def Search(update, _):
    """ Записывает поступившее сообщение и запускает вывод по запросу поиска
    args -> update message
    return -> завершение ConversationHandler
    """
    user = update.message.from_user
    if checks.Check_name(update) == False: return SEARCH
    # if checks.Check_none(update) == False: return SEARCH
    logger.info("Пользователь %s искал: %s", user.first_name, update.message.text)
    update.message.reply_text(f'{controller.Search_contact(update)} \n''Для перехода в меню отправьте /start')
    return ConversationHandler.END 

def Delete(update, _):
    """ Записывает поступившее сообщение и запускает сообщение в телеграм для удаления контакта
    args -> update message
    return -> int (переход на следующий шаг по списку)
    """
    user = update.message.from_user
    logger.info("Пользователь %s удалил контакт: %s", user.first_name, update.message.text)
    if checks.Check_name(update) == False: return DELETE
    # if checks.Check_none(update) == False: return DELETE
    update.message.reply_text(f'{controller.Search_contact(update)} \n''Введите номер телефона контакта для удаления\n')
    return DELETE_SECOND
   

def Delete_second(update, _):
    """Второй шаг для удаления контакта
    args -> update message
    return -> завершение ConversationHandler
    """
    if checks.Check_num(update) == False: return DELETE_SECOND
    # if checks.Check_phone_del(update) == False: return DELETE_SECOND
    controller.Delete_contact(update)
    update.message.reply_text('Контакт удален \n''Для перехода в меню отправьте /start')
    return ConversationHandler.END  

def Cancel(update, _):
    """ Записывает поступившее сообщение с командой отмены 
    args -> update message
    return -> завершение ConversationHandler
    """
    user = update.message.from_user
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    update.message.reply_text('Мое дело предложить - Ваше отказаться \n' 'Для перехода в меню отправьте /start', reply_markup=ReplyKeyboardRemove(),)
    return ConversationHandler.END


def main():
    """ Основной алгоритм ConversationHandler
    args -> None
    return -> None
    """
   
    updater = Updater(TOKEN)
  
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
       
        states={
            CHOICE: [MessageHandler(Filters.regex('^(Добавить контакт|Найти контакт|Удалить контакт)$'), Choice)],
            STEP_NAME: [MessageHandler(Filters.text & ~Filters.command, Name)],
            STEP_LAST_NAME: [MessageHandler(Filters.text & ~Filters.command, Last_name)],
            STEP_PHONE_NUM: [MessageHandler(Filters.text & ~Filters.command, Phone_num)],
            STEP_GROUP: [MessageHandler(Filters.text & ~Filters.command, Group), CommandHandler('skip', skip_group)],
            STEP_COMMENT: [MessageHandler(Filters.text & ~Filters.command, Comment), CommandHandler('skip', skip_comment)],
            SEARCH: [MessageHandler(Filters.text & ~Filters.command, Search)],
            DELETE: [MessageHandler(Filters.text & ~Filters.command, Delete)],
            DELETE_SECOND: [MessageHandler(Filters.text & ~Filters.command, Delete_second)]
        },
        fallbacks=[CommandHandler('cancel', Cancel)],
    )

  
    dispatcher.add_handler(conv_handler)

   
    updater.start_polling()
    updater.idle()


