import logging

from database import connection
from utils import selection_date, payments_data, excel_write, region_data, store_data, seller_data, device_data
import time
import schedule


# Автоматизация импорта данных и сформирования в эксель 2 раза в сутки
def insert_data(name, path, operation, period):
    cursor = connection.cursor()
    query = f"""
        INSERT INTO excel_report (name, path, operation, period)
        VALUES ({name}, {path}, {operation}, {period})' 
            """
    cursor.execute(query)
    connection.commit()


def import_report():
    type_operation = ['payments', 'regions', 'stores', 'sellers', 'devices']
    period_list = ['yesterday', 'today', 'week', 'month']
    for type_op in type_operation:
        for period in period_list:
            date = selection_date(period)  # Возвращает дату и строку даты
            if type_op == 'payments':
                payments = payments_data(date[0])
                logging.info('payments_unfo: , %r', payments)
                filepath, filename = excel_write(payments, type_op, date[1])
                insert_data(filename, filepath, type_op, period)
            elif type_op == 'regions':
                regions = region_data(date[0])
                filepath, filename = excel_write(regions, type_op, date[1])
                insert_data(filename, filepath, type_op, period)
            elif type_op == 'stores':
                stores = store_data(date[0])
                filepath, filename = excel_write(stores, type_op, date[1])
                insert_data(filename, filepath, type_op, period)
            elif type_op == 'sellers':
                seller = seller_data(date[0])
                filepath, filename = excel_write(seller, type_op, date[1])
                insert_data(filename, filepath, type_op, period)
            elif type_op == 'devices':
                devices = device_data(date[0])
                filepath, filename = excel_write(devices, type_op, date[1])
                insert_data(filename, filepath, type_op, period)
            else:
                error = 'ЧТО-ТО ПОШЛО НЕ ТАК!'
                logging.info("ERROR", error)


import_report()


# schedule.every(5).minutes.do(import_report)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
