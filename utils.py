import logging
from datetime import datetime, timedelta
from database import server, cursor, connection
import pandas as pd
import openpyxl
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


def payments_data(date):  # Вывод данных по фин партнерам
    # server.start()
    query = f"""
        SELECT ox_payments.name as name,
        COUNT(ox_sell_transactions.ox_payment_id) AS quantity_sale,
        SUM(ox_sell_transactions.price * CASE WHEN ox_sell_transactions.ox_payment_id = 15 THEN 12 ELSE 1 END) as total_price
        FROM ox_sell_transactions 
        JOIN ox_payments
        ON ox_sell_transactions.ox_payment_id=ox_payments.id
        WHERE DATE(ox_sell_transactions."time") BETWEEN '{date}' AND CURRENT_DATE 
        AND status = 'finished' 
        AND ox_sell_transactions."type"='sell'
        GROUP BY ox_payments."name" 
        ORDER BY total_price DESC """
    cursor.execute(query)
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        data[row[0]] = (row[1], row[2], date + " 00:00", datetime.today().strftime('%Y-%m-%d %H:%M'))
    # server.stop()
    # cursor.close()
    # connection.close()
    return data


def region_data(date):  # Вывод данных по областям
    # server.start()
    query = f"""
        SELECT ox_locations."administrativeArea" as name,
        COUNT(ox_locations."id") as quantity_sale,
        SUM(ox_sell_transactions.price * CASE WHEN ox_sell_transactions.ox_payment_id = 15 THEN 12 ELSE 1 END) as total_price
        FROM ox_sell_transactions
        INNER JOIN ox_sell_records
        ON ox_sell_transactions.ox_sell_id = ox_sell_records.ox_sell_id
        INNER JOIN ox_locations
        ON ox_sell_records.ox_location_id = ox_locations.id
        WHERE ox_sell_transactions."type"='sell'
        AND DATE(ox_sell_transactions."time") BETWEEN '{date}' AND CURRENT_DATE
        AND status='finished'
        AND ox_locations."type"='shop'
        GROUP BY ox_locations."administrativeArea"
        ORDER BY total_price DESC """
    cursor.execute(query)
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        data[row[0]] = (row[1], row[2], date + " 00:00", datetime.today().strftime('%Y-%m-%d %H:%M'))
    # server.stop()
    # cursor.close()
    # connection.close()
    return data


def store_data(date):  # Вывод ТОП-10 по торговым точкам
    # server.start()
    query = f"""
        SELECT subquery.*
        FROM (
        SELECT ox_locations."name" as name,
        COUNT(ox_locations."id") as quantity_sale, 
        SUM(ox_sell_transactions.price * CASE WHEN ox_sell_transactions.ox_payment_id = 15 THEN 12 ELSE 1 END) as total_price
        FROM "ox_sell_transactions"
        INNER JOIN ox_sell_records
        ON ox_sell_transactions.ox_sell_id = ox_sell_records.ox_sell_id
        INNER JOIN ox_locations
        ON ox_sell_records.ox_location_id = ox_locations."id"
        WHERE ox_sell_transactions."type"='sell' 
        AND DATE(ox_sell_transactions."time") BETWEEN '{date}' AND CURRENT_DATE
        AND ox_sell_transactions."status" = 'finished'
        AND ox_locations."type" = 'shop'
        GROUP BY ox_locations."name"
        ORDER BY total_price DESC
        LIMIT 10) AS subquery """
    cursor.execute(query)
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        data[row[0]] = (row[1], row[2], date + " 00:00", datetime.today().strftime('%Y-%m-%d %H:%M'))
    # server.stop()
    # cursor.close()
    # connection.close()
    return data


def seller_data(date):  # Вывод ТОП-10 по продавцам
    # server.start()
    query = f"""
        SELECT subquery.*
        FROM (
        SELECT (ox_users."firstName" || ' ' || ox_users."lastName") as name,
        COUNT(ox_users."id") as quantity_sale,  
        SUM(ox_sell_transactions.price * CASE WHEN ox_sell_transactions.ox_payment_id = 15 THEN 12 ELSE 1 END) as total_price,
        ox_locations."name" as store 
        FROM ox_users
        INNER JOIN ox_sells
        ON ox_users."id" = ox_sells.ox_user_id
        INNER JOIN ox_sell_records
        ON ox_sells."id" = ox_sell_records.ox_sell_id
        INNER JOIN ox_sell_transactions
        ON ox_sells."id" = ox_sell_transactions.ox_sell_id
        INNER JOIN ox_locations
        ON ox_sell_records.ox_location_id = ox_locations."id"
        WHERE DATE(ox_sell_transactions."time") BETWEEN '{date}' AND CURRENT_DATE 
        AND ox_sell_transactions."type" ='sell'
        AND ox_sell_transactions.status = 'finished'
        AND ox_locations."type" = 'shop'
        GROUP BY ox_users."firstName", ox_users."lastName", ox_locations."name"
        ORDER BY total_price DESC
        LIMIT 10) AS subquery """
    cursor.execute(query)
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        data[row[0]] = (row[1], row[2], date + " 00:00", datetime.today().strftime('%Y-%m-%d %H:%M'))
    # server.stop()
    # cursor.close()
    # connection.close()
    return data


def device_data(date):  # Вывод ТОП-10 по девайсам
    # server.start()
    query = f"""
        SELECT subquery.*
        FROM (
        SELECT ox_variants."name" as name,
        COUNT(ox_variants."id") as quantity_sale, 
        SUM(ox_sell_transactions.price * CASE WHEN ox_sell_transactions.ox_payment_id = 15 THEN 12 ELSE 1 END) as total_price
        FROM ox_variants
        INNER JOIN ox_sell_records
        ON ox_variants."id" = ox_sell_records.ox_variant_id
        INNER JOIN ox_sell_transactions
        ON ox_sell_transactions.ox_sell_id = ox_sell_records.ox_sell_id
        WHERE DATE(ox_sell_transactions."time") BETWEEN '{date}' AND CURRENT_DATE
        AND ox_sell_transactions."type"='sell'
        AND ox_sell_transactions.status='finished'
        GROUP BY device
        ORDER BY total_price DESC
        LIMIT 10) AS subquery """
    cursor.execute(query)
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        data[row[0]] = (row[1], row[2], date + " 00:00", datetime.today().strftime('%Y-%m-%d %H:%M'))
    # server.stop()
    # cursor.close()
    # connection.close()
    return data


def selection_date(period):  # Выбор периода: день, неделя, месяц
    now = datetime.today()

    if period == 'yesterday':
        yesterday = datetime.now() - timedelta(days=1)
        str_name = 'За вчера'
        return yesterday.strftime("%Y-%m-%d"), str_name
    elif period == 'today':
        str_name = 'За сегодня'
        return now.strftime("%Y-%m-%d"), str_name
    elif period == 'week':
        start_of_week = now - timedelta(days=now.weekday())
        str_name = 'За текущую неделю'
        return start_of_week.strftime("%Y-%m-%d"), str_name
    elif period == 'month':
        start_of_month = datetime(now.year, now.month, 1)
        str_name = 'За текущий месяц'
        return start_of_month.strftime("%Y-%m-%d"), str_name


def excel_write(data, type_operation, period):
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Количество продаж', 'Общая сумма', 'Начало даты', 'Конец даты'])
    logging.info('df_info: %r', df)
    filename = f"Отчёт|{type_operation}|{period}|{current_date}.xlsx"
    filepath = f'/home/report/web/report.smartblax.uz/public_html/uploads/{filename}'
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
    excel_file_path = cursor.fetchone()
    logging.info('path: %r', excel_file_path)
    excel_file_path = os.path.normpath(excel_file_path[0])
    logging.info('path_new: %r', excel_file_path)
    df = pd.read_excel(excel_file_path)
    new_data = {}
    text_file = f'<b>Отчёт: по фин партнерам </b>\n<b>Период: за вчера</b>\n\n'
    for index, device in df[f'{operation}'].items():
        sales = int(df['Количество продаж'][index])
        total_price = int(df['Общая сумма'][index])
        formatted_total_price = '{:,}'.format(total_price).replace(',', ' ')
        text_file += f'<b>{device}:</b> \nКоличество продаж: {sales} \nОбщая сумма: {formatted_total_price} сум\n\n'
    return text_file


# def text_out(result):
#     text_file = f'<b>Отчёт: {result[1]}</b>\n<b>Период: {result[2]}</b>\n\n'
#     if not result[0]:
#         text_file += 'Данные будут обновленны после 12:00'
#         return text_file
#     else:
#         for keys, values in result[0].items():
#             text_file += f'<b>{keys}:</b> \nКоличество продаж: {values[0]} \nОбщая сумма: {values[1]:,} сум\n\n'
#         return text_file


# def action(numb, period):
#     date_func = selection_date(period)
#     if numb == 'payments':
#         partners = payments_data(date_func[0])
#         self_name = 'По фин.партнерам'
#         str_date = date_func[1]
#         return partners, self_name, str_date
#     elif numb == 'regions':
#         regions = region_data(date_func[0])
#         self_name = 'По областям'
#         str_name = date_func[1]
#         return regions, self_name, str_name
#     elif numb == 'stores':
#         locations = store_data(date_func[0])
#         self_name = 'ТОП-10 торговых точек'
#         str_name = date_func[1]
#         return locations, self_name, str_name
#     elif numb == 'sellers':
#         seller = seller_data(date_func[0])
#         self_name = 'ТОП-10 продавцов'
#         str_name = date_func[1]
#         return seller, self_name, str_name
#     elif numb == 'devices':
#         devices = device_data(date_func[0])
#         self_name = 'ТОП-10 девайсов'
#         str_name = date_func[1]
#         return devices, self_name, str_name
