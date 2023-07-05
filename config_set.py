# Файл конфигурации, в котором хранятся различные параметры и настройки вашего бота,
# такие как токен API Telegram, настройки базы данных и другие конфигурационные параметры.

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()

