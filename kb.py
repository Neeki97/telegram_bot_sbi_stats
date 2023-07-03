from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

phone_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Поделиться номером', request_contact=True)]],
                            resize_keyboard=True,
                            input_field_placeholder='Без номера никуда!')


operation_button = [
    [InlineKeyboardButton(text='Данные по всем фин. партнерам', callback_data='payments')],
    [InlineKeyboardButton(text='Данные по областям', callback_data='regions')],
    [InlineKeyboardButton(text='ТОП-10 локаций', callback_data='stores')],
    [InlineKeyboardButton(text='ТОП-10 продавцов', callback_data='sellers')],
    [InlineKeyboardButton(text='ТОП-10 девайсов', callback_data='devices')]
]
operation = InlineKeyboardMarkup(inline_keyboard=operation_button)


period_button = [
    [InlineKeyboardButton(text='За день', callback_data='today')],
    [InlineKeyboardButton(text='За вчера', callback_data='yesterday')],
    [InlineKeyboardButton(text='За текущую неделю', callback_data='week')],
    [InlineKeyboardButton(text='За текущий месяц', callback_data='month')],
    [InlineKeyboardButton(text='Вернуться к операциям', callback_data='cancel')]
]
period = InlineKeyboardMarkup(inline_keyboard=period_button)


excel_button = [
    [InlineKeyboardButton(text='Сформировать excel-файл', callback_data='excel')],
    [InlineKeyboardButton(text='Выбрать отчёт', callback_data='Выбрать отчёт')]
]
excel = InlineKeyboardMarkup(inline_keyboard=excel_button)


start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Выбрать отчёт')]],
                            resize_keyboard=True,
                            input_field_placeholder='Нажмите кнопку для выбора отчёта')
