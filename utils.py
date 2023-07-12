import logging
import re
from datetime import datetime
from database import cursor, connection
import pandas as pd
from aiogram.types import FSInputFile
import requests
import os
import io
from dotenv import load_dotenv, find_dotenv


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
    text_file = f'<b>Отчёт: {str_operation(operation)}\nПериод: {str_period(period)}</b>\n\n'
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


def subscriptions_data(operation, period):
    load_dotenv(find_dotenv())
    auth = (os.environ.get('auth_username'), os.environ.get('auth_password'))
    query_params = {'period': f'{period}'}
    base_url = f'https://api-server.retailbox.uz/api/v1/exchange/dashboard/subscription/{operation}'
    response = requests.get(base_url, auth=auth, params=query_params)
    if response.status_code == 200:
        if operation == 'stats':
            data = response.json()
            text_file = f'<b>Отчёт: Общие данные по подписке\nПериод: {str_period(period)}</b> \n\n'
            lst_data = data['data']
            subscription_count = lst_data[0]['value']
            subscription_done = lst_data[3]['value']
            subscriptions_sum_product_price = lst_data[5]['value']
            formatted_total_price = '{:,}'.format(subscriptions_sum_product_price).replace(',', ' ')
            text_file += f"Всего запросов по подписке: {subscription_count}\nВсего оформлено подписок: {subscription_done}\nОбщая сумма продаж: {formatted_total_price} сум\n"
            logging.info('text: %r', text_file)
            return text_file
        elif operation in ['users', 'shops']:
            data = response.json()
            text_file = f'<b>Отчёт: {str_operation(operation)}\nПериод: {str_period(period)}</b> \n\n'
            for values in data['data']:
                name = values['name']
                subscription_count = values['subscriptions_count']
                subscription_done = values['subscriptions_done']
                owner_tickers_count = values['owner_tickets_count']
                subscriptions_sum_product_price = values['subscriptions_sum_product_price']
                formatted_total_price = '{:,}'.format(subscriptions_sum_product_price).replace(',', ' ')
                text_file += f"""<b>{name}</b>\nВсего запросов по подписке: {subscription_count}\nВсего оформлено подписок: {subscription_done}\nВсего ошибок в оформлении подписок: {owner_tickers_count}\nОбщая сумма продаж: {formatted_total_price} сум \n\n"""
            logging.info('text: %r', text_file)
            return text_file
        elif operation == 'variants':
            data = response.json()
            text_file = f'<b>Отчёт: {str_operation(operation)}\nПериод: {str_period(period)}</b> \n\n'
            for values in data['data']:
                name = values['name']
                subscription_count = values['subscriptions_count']
                subscription_done = values['subscriptions_done']
                subscriptions_sum_product_price = values['subscriptions_sum_product_price']
                formatted_total_price = '{:,}'.format(subscriptions_sum_product_price).replace(',', ' ')
                text_file += f"""<b>{name}</b>\nВсего запросов по подписке: {subscription_count}\nВсего оформлено подписок: {subscription_done}\nОбщая сумма продаж: {formatted_total_price} сум \n\n"""
            logging.info('text: %r', text_file)
            return text_file
    else:
        logging.info('Ошибка при выполнении запроса: %r', response.status_code)


def str_operation(operation):
    if operation == 'payments':
        str_op = 'По платежам'
        return str_op
    elif operation == 'regions':
        str_op = 'По областям'
        return str_op
    elif operation in ['stores', 'shops']:
        str_op = 'По торговым точкам'
        return str_op
    elif operation in ['sellers', 'users']:
        str_op = 'ТОП-10 продавцов'
        return str_op
    elif operation == 'devices':
        str_op = 'ТОП-10 девайсов'
        return str_op
    elif operation == 'variants':
        str_op = 'По смартфонам'
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


# def test(operation, period):
#     logging.info('test_stats: %r', operation, period)
#     load_dotenv(find_dotenv())
#     auth = (os.environ.get('auth_username'), os.environ.get('auth_password'))
#     query_params = {'period': f'{period}'}
#     base_url = f'https://api-server.retailbox.uz/api/v1/exchange/dashboard/subscription/{operation}'
#     response = requests.get(base_url, auth=auth, params=query_params)
#     data = response.json()
#     lst = data['data']
#     if operation == 'stats':
#         new_dict = {}
#         for item in lst:
#             new_dict[item['title']] = item['value']
#         df = pd.DataFrame.from_dict(new_dict, orient='index')
#         exl_buffer = io.BytesIO()
#         df.to_excel('example.xlsx', index=False)
#         return exl_buffer.seek(0)
#     else:
#         return 'выбрал не то!'