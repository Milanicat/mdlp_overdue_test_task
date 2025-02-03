from app.process_files import upload_file_overdue_to_db, create_report_overdue

from app.bot import bot


# Название файла, который необходимо обработать
overdue_file_name = 'Просрочено (06.09.2022).xlsx'


@bot.message_handler(commands=['overdue_to_db'])
def overdue_to_db(message):
    result_message = upload_file_overdue_to_db(overdue_file_name)
    bot.send_message(message.chat.id, result_message)


@bot.message_handler(commands=['report'])
def send_report_overdue(message):
    report = create_report_overdue(overdue_file_name)
    bot.send_document(message.chat.id, report)
