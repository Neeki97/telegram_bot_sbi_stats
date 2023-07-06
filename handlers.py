# Этот файл содержит обработчики различных типов сообщений, которые ваш бот может получать.
# Здесь вы можете определить функции для обработки текстовых сообщений, команд, изображений, аудиофайлов и других типов медиа.

import logging

from aiogram import types, Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils import autenfication_number, excel_read, uploads_excel


import kb
import text
from states import Form

router = Router()


@router.message(Command('start'))
async def number_user(msg: types.Message):
    await msg.answer('Нажмите на кнопку <b>"Поделиться номером"</b>', reply_markup=kb.phone_number)


@router.message(F.contact)
async def autenfication_user(msg: types.Message):
    phone = msg.contact.phone_number
    chat_id = msg.chat.id
    firstname = msg.contact.first_name
    lastname = msg.contact.last_name
    username = msg.chat.username
    # logging.info("phone: %r", phone)
    # logging.info("chat_id: %r", chat_id)
    # logging.info("firstname: %r", firstname)
    # logging.info("lastname: %r", lastname)
    # logging.info("username: %r", username)
    if autenfication_number(phone, chat_id, firstname, lastname, username):
        await msg.reply(text='Отлично! У вас есть доступ!', reply_markup=types.ReplyKeyboardRemove())
        await msg.answer(text.menu, reply_markup=kb.operation)
    else:
        await msg.reply('Извините у вас нет доступа !')


@router.callback_query(F.data.in_({'Выбрать отчёт'}))
async def start_handler(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.menu.format(), reply_markup=kb.operation)


@router.callback_query(F.data.in_({'payments', 'regions', 'stores', 'sellers', 'devices'}))
async def input_operation(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Form.operation)
    await state.clear()
    operation = await state.update_data(operation=clbck.data)
    logging.info('operation: %r', operation)
    await clbck.message.delete_reply_markup()
    await state.set_state(Form.period)
    await clbck.message.edit_text(text.date, reply_markup=kb.period)


@router.callback_query(Form.period, F.data.in_({'today', 'yesterday', 'week', 'month', 'cancel', 'excel'}))
async def input_period(clbck: CallbackQuery, state: FSMContext):
    lst_period = 'today', 'yesterday', 'week', 'month'
    cancel_button = 'cancel'
    excel_button = 'excel'
    if clbck.data == cancel_button:
        state = await state.clear()
        # logging.info('state_clear: %r', state)
        await clbck.message.edit_text(text.menu, reply_markup=kb.operation)
    elif clbck.data in lst_period:
        state = await state.update_data(period=clbck.data)
        logging.info('state_update: %r', state)
        text_report = excel_read(state.get('operation'), state.get('period'))
        # await clbck.message.edit_text(text.date_selected)
        # data = action(state.get('operation'), state.get('period'))
        # logging.info("DATA: %r", data[0])
        # excel_file(data)
        # text_result = text_out(data)
        await clbck.message.edit_text(text=text_report, reply_markup=kb.upload_excel)
    elif clbck.data == excel_button:
        state = await state.get_data()
        # logging.info('log_state: %r', state)
        file = uploads_excel(state['operation'], state['period'])
        await clbck.message.answer_document(caption='Файл готов! ', document=file)
    chat_id = clbck.message.chat.id
    logging.info('user_chat_id: %r', chat_id)


@router.message(F.text)
async def excel_convert(msg: types.Message):
    await msg.answer('Нажимайте кнопочки!')
