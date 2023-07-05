# Этот файл содержит функции для чтения, записи и обновления данных в базе данных,
# например, для хранения настроек пользователя или сохранения промежуточных результатов.

import psycopg2
from sshtunnel import SSHTunnelForwarder
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
server = SSHTunnelForwarder(
    ssh_host=os.environ.get('ssh_host'),
    ssh_port=os.environ.get('ssh_port'),
    ssh_username=os.environ.get('ssh_username'),
    ssh_password=os.environ.get('ssh_password'),
    remote_bind_address=('127.0.0.1', 5432)
)
server.start()


connection = psycopg2.connect(
    host=os.environ.get('db_host'),
    port=server.local_bind_port,
    dbname=os.environ.get('db_name'),
    user=os.environ.get('db_user'),
    password=os.environ.get('db_password')
    )

# connection.set_session(autocommit=True)
cursor = connection.cursor()
