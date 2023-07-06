import logging
import re
from datetime import datetime
from database import cursor, connection
import pandas as pd
from aiogram.types import FSInputFile


def autenfication_number(phone, chat_id, firstname, lastname, username):
    phone = re.sub(r'\D', '', phone)
    query = """
        SELECT * FROM telegram_users WHERE phonenumber= %s """
    cursor.execute(query, (phone,))
    result = cursor.fetchall()
    logging.info('User_info from db: %r', result)
    if result:
        query = """
        UPDATE telegram_users
        SET chat_id=%s, firstname=%s, lastname=%s, username=%s
        WHERE phonenumber=%s """
        cursor.execute(query, (chat_id, firstname, lastname, username, phone))
        connection.commit()
        return True
    else:
        return False


def excel_write(data, type_operation, period):
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Количество продаж', 'Общая сумма', 'Начало даты', 'Конец даты'])
    # logging.info('excel_write: %r', df)
    filename = f'Отчёт_{type_operation}_{period}_{current_date.replace("-", "_")}.xlsx'
    filepath = f'loads//{filename}'
    df.to_excel(filepath, index_label=f'{type_operation}')
    return filepath, filename


def excel_read(operation, period):
    query = f"""
            SELECT path 
            FROM import_excel
            WHERE operation = '{operation}' AND period = '{period}'
            ORDER BY created_at DESC
            LIMIT 1 """
    cursor.execute(query)
    excel_file_path = cursor.fetchone()[0]
    # logging.info('path: %r', excel_file_path)
    df = pd.read_excel(excel_file_path)
    text_file = f'<b>Отчёт: {str_operation(operation)}</b>\n<b>Период: {str_period(period)}</b>\n\n'
    for index, device in df[f'{operation}'].items():
        sales = int(df['Количество продаж'][index])
        total_price = int(df['Общая сумма'][index])
        formatted_total_price = '{:,}'.format(total_price).replace(',', ' ')
        text_file += f'<b>{device}:</b> \nКоличество продаж: {sales} \nОбщая сумма: {formatted_total_price} сум\n\n'
    return text_file


def uploads_excel(operation, period):
    query = f"""
            SELECT path 
            FROM import_excel
            WHERE operation = '{operation}' AND period = '{period}'
            ORDER BY created_at DESC
            LIMIT 1 """
    cursor.execute(query)
    path = cursor.fetchone()[0]
    logging.info('upld_ex_path: %r', path)
    file = FSInputFile(path)
    return file


def str_operation(operation):
    if operation == 'payments':
        str_op = 'По платежам'
        return str_op
    elif operation == 'regions':
        str_op = 'По областям'
        return str_op
    elif operation == 'stores':
        str_op = 'По торговым точкам'
        return str_op
    elif operation == 'sellers':
        str_op = 'ТОП-10 продавцов'
        return str_op
    elif operation == 'devices':
        str_op = 'ТОП-10 девайсов'
        return str_op


def str_period(period):
    if period == 'today':
        str_per = 'За сегоднящний день'
        return str_per
    elif period == 'yesterday':
        str_per = 'За вчерашний день'
        return str_per
    elif period == 'week':
        str_per = 'За текущую неделю'
        return str_per
    elif period == 'month':
        str_per = 'За текущий месяц'
        return str_per
