from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

phone_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Поделиться номером', request_contact=True)]],
                            resize_keyboard=True,
                            input_field_placeholder='Без номера никуда!')


menu_btn = [
    [InlineKeyboardButton(text='Данные по всем продажам', callback_data='all records')],
    [InlineKeyboardButton(text='Смартфон по подписке', callback_data='subscriptions')]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu_btn)


subscriptions_button = [
    [InlineKeyboardButton(text='Общие данные', callback_data='stats')],
    [InlineKeyboardButton(text='ТОП-10 локаций', callback_data='shops')],
    [InlineKeyboardButton(text='ТОП-10 продавцов', callback_data='users')],
    [InlineKeyboardButton(text='Данные по смартфонам', callback_data='variants')],
    [InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')]
]
subscriptions = InlineKeyboardMarkup(inline_keyboard=subscriptions_button)


operation_button = [
    [InlineKeyboardButton(text='Данные по всем продажам', callback_data='payments')],
    [InlineKeyboardButton(text='Данные по областям', callback_data='regions')],
    [InlineKeyboardButton(text='ТОП-10 локаций', callback_data='stores')],
    [InlineKeyboardButton(text='ТОП-10 продавцов', callback_data='sellers')],
    [InlineKeyboardButton(text='ТОП-10 девайсов', callback_data='devices')],
    [InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')]
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
    [InlineKeyboardButton(text='Перейти в меню', callback_data='menu')]
]
excel = InlineKeyboardMarkup(inline_keyboard=excel_button)


# start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Выбрать отчёт')]],
#                             resize_keyboard=True,
#                             input_field_placeholder='Нажмите кнопку для выбора отчёта')
