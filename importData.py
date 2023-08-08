import logging
from datetime import datetime, timedelta

from database import cursor
from database import connection
from utils import excel_write


def payments_data(start_date, end_date):  # Вывод данных по фин партнерам
    # server.start()
    query = f"""
        SELECT ox_payments.name as name,
        COUNT(ox_sell_transactions.ox_payment_id) AS quantity_sale,
        SUM(ox_sell_transactions.price * CASE WHEN ox_sell_transactions.ox_payment_id = 15 THEN 12 ELSE 1 END) as total_price
        FROM ox_sell_transactions 
        JOIN ox_payments
        ON ox_sell_transactions.ox_payment_id=ox_payments.id
        WHERE DATE(ox_sell_transactions."time") BETWEEN '{start_date}' AND '{end_date}' 
        AND status = 'finished' 
        GROUP BY ox_payments."name" 
        ORDER BY total_price DESC """
    cursor.execute(query)
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        data[row[0]] = (row[1], row[2], start_date + " 00:00", end_date)
    # server.stop()
    # cursor.close()
    # connection.close()
    return data


def region_data(start_date, end_date):  # Вывод данных по областям
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
        WHERE DATE(ox_sell_transactions."time") BETWEEN '{start_date}' AND '{end_date}' AND ox_locations.ox_brand_id = 1
        AND status='finished'
        AND ox_locations."type"='shop'
        GROUP BY ox_locations."administrativeArea"
        ORDER BY total_price DESC """
    cursor.execute(query)
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        data[row[0]] = (row[1], row[2], start_date + " 00:00", end_date)
    # server.stop()
    # cursor.close()
    # connection.close()
    return data


def store_data(start_date, end_date):  # Вывод ТОП-10 по торговым точкам
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
        WHERE DATE(ox_sell_transactions."time") BETWEEN '{start_date}' AND '{end_date}' AND ox_locations.ox_brand_id = 1
        AND ox_sell_transactions."status" = 'finished'
        AND ox_locations."type" = 'shop'
        GROUP BY ox_locations."name"
        ORDER BY total_price DESC
        LIMIT 10) AS subquery """
    cursor.execute(query)
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        data[row[0]] = (row[1], row[2], start_date + " 00:00", end_date)
    # server.stop()
    # cursor.close()
    # connection.close()
    return data


def seller_data(start_date, end_date):  # Вывод ТОП-10 по продавцам
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
        WHERE DATE(ox_sell_transactions."time") BETWEEN '{start_date}' AND '{end_date}' AND ox_locations.ox_brand_id = 1
        AND ox_sell_transactions.status = 'finished'
        AND ox_locations."type" = 'shop'
        GROUP BY ox_users."firstName", ox_users."lastName", ox_locations."name"
        ORDER BY total_price DESC
        LIMIT 10) AS subquery """
    cursor.execute(query)
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        data[row[0]] = (row[1], row[2], start_date + " 00:00", end_date)
    # server.stop()
    # cursor.close()
    # connection.close()
    return data


def device_data(start_date, end_date):  # Вывод ТОП-10 по девайсам
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
        WHERE DATE(ox_sell_transactions."time") BETWEEN '{start_date}' AND '{end_date}' 
        AND ox_sell_transactions.status='finished'
        GROUP BY ox_variants."name"
        ORDER BY total_price DESC
        LIMIT 10) AS subquery """
    cursor.execute(query)
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        data[row[0]] = (row[1], row[2], start_date + " 00:00", end_date)
    # server.stop()
    # cursor.close()
    # connection.close()
    return data


def selection_date(period):  # Выбор периода: день, неделя, месяц
    now = datetime.today()
    if period == 'yesterday':
        yesterday = datetime.now() - timedelta(days=1)
        str_name = 'За вчера'
        return yesterday.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d") + " 23:59:59", str_name
    elif period == 'today':
        str_name = 'За сегодня'
        return now.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d %H:%M:%S"), str_name
    elif period == 'week':
        start_of_week = now - timedelta(days=now.weekday())
        str_name = 'За текущую неделю'
        return start_of_week.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d %H:%M:%S"), str_name
    elif period == 'month':
        start_of_month = datetime(now.year, now.month, 1)
        str_name = 'За текущий месяц'
        return start_of_month.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d %H:%M:%S"), str_name


# Автоматизация импорта данных и сформирования в эксель 2 раза в сутки
def insert_data(name, path, operation, period):
    query = f"""
        INSERT INTO import_excel (name, path, operation, period)
        VALUES ('{name}', '{path}', '{operation}', '{period}') 
            """
    cursor.execute(query)
    connection.commit()


def import_report():
    type_operation = ['payments', 'regions', 'stores', 'sellers', 'devices']
    period_list = ['yesterday', 'today', 'week', 'month']
    for type_op in type_operation:
        for period in period_list:
            date = selection_date(period)  # Возвращает начало периода, конец периода и строку даты
            if type_op == 'payments':
                payments = payments_data(date[0], date[1])
                filepath, filename = excel_write(payments, type_op, date[2])
                insert_data(name=filename, path=filepath, operation=type_op, period=period)
            elif type_op == 'regions':
                regions = region_data(date[0], date[1])
                filepath, filename = excel_write(regions, type_op, date[2])
                insert_data(filename, filepath, type_op, period)
            elif type_op == 'stores':
                stores = store_data(date[0], date[1])
                filepath, filename = excel_write(stores, type_op, date[2])
                insert_data(filename, filepath, type_op, period)
            elif type_op == 'sellers':
                seller = seller_data(date[0], date[1])
                filepath, filename = excel_write(seller, type_op, date[2])
                insert_data(filename, filepath, type_op, period)
            elif type_op == 'devices':
                devices = device_data(date[0], date[1])
                filepath, filename = excel_write(devices, type_op, date[2])
                insert_data(filename, filepath, type_op, period)


import_report()


