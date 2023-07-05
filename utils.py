import logging
from datetime import datetime, timedelta
from database import server, cursor, connection
import pandas as pd
from aiogram.types import FSInputFile

import os


def autenfication_number(phone, chat_id, firstname, lastname, username):
    query = f"""
        SELECT * FROM telegram_users WHERE phonenumber='{phone}' """
    cursor.execute(query)
    result = cursor.fetchall()
    logging.info('result: %r', result)
    if result:
        query = f"""
        UPDATE telegram_users
        SET chat_id='{chat_id}', firstname='{firstname}', lastname='{lastname}', username='{username}'
        WHERE phonenumber='{phone}' """
        cursor.execute(query)
        connection.commit()
        return True
    else:
        return False


def excel_write(data, type_operation, period):
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Количество продаж', 'Общая сумма', 'Начало даты', 'Конец даты'])
    logging.info('df_info: %r', df)
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
    # excel_file_path = os.path.normpath(excel_file_path[0])
    # logging.info('path_new: %r', excel_file_path)
    df = pd.read_excel(excel_file_path)
    new_data = {}
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
