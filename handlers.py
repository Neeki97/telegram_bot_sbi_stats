# Этот файл содержит обработчики различных типов сообщений, которые ваш бот может получать.
# Здесь вы можете определить функции для обработки текстовых сообщений, команд, изображений, аудиофайлов и других типов медиа.

import logging

from aiogram import types, Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils import autenfication_number, excel_read, uploads_excel, subscriptions_data


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
        await msg.answer(text='start menu', reply_markup=kb.menu)
    else:
        await msg.reply('Извините, у Вас нет доступа !')


@router.callback_query(F.data.in_({'all records', 'subscriptions'}))
async def main_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Form.menu)
    # await state.clear()
    state_menu = await state.update_data(menu=clbck.data)
    logging.info('menu: %r', state_menu.get('menu'))
    await clbck.message.delete_reply_markup()
    await state.set_state(Form.operation)
    if state_menu.get('menu') == 'all records':
        await clbck.message.edit_text(text=text.menu, reply_markup=kb.operation)
    elif state_menu.get('menu') == 'subscriptions':
        await clbck.message.edit_text(text=text.menu, reply_markup=kb.subscriptions)


@router.callback_query(F.data.in_({'menu'}))
async def start_handler(clbck: CallbackQuery):
    await clbck.message.edit_text(text.menu.format(), reply_markup=kb.menu)


@router.callback_query(F.data.in_({'all records'}))
async def start_handler(clbck: CallbackQuery):
    await clbck.message.edit_text(text.menu.format(), reply_markup=kb.operation)


@router.callback_query(F.data.in_({'subscriptions'}))
async def subscriptions_menu(clbck: CallbackQuery):
    await clbck.message.edit_text(text='подписка меню', reply_markup=kb.subscriptions)


@router.callback_query(F.data.in_({'stats', 'users', 'shops', 'variants'}))
async def input_subscriptions(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Form.operation)
    # await state.clear()
    state_operation = await state.update_data(operation=clbck.data)
    logging.info('operation: %r', state_operation)
    await clbck.message.delete_reply_markup()
    await state.set_state(Form.period)
    await clbck.message.edit_text(text=text.date, reply_markup=kb.period)


@router.callback_query(F.data.in_({'payments', 'regions', 'stores', 'sellers', 'devices'}))
async def input_operation(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Form.operation)
    # await state.clear()
    state_operation = await state.update_data(operation=clbck.data)
    logging.info('operation: %r', state_operation)
    await clbck.message.delete_reply_markup()
    await state.set_state(Form.period)
    await clbck.message.edit_text(text.date, reply_markup=kb.period)


@router.callback_query(Form.period, F.data.in_({'today', 'yesterday', 'week', 'month', 'cancel'}))
async def input_period(clbck: CallbackQuery, state: FSMContext):
    lst_period = 'today', 'yesterday', 'week', 'month'
    cancel_button = 'cancel'
    if clbck.data == cancel_button:
        state = await state.get_data()
        if state.get('menu') == 'all records':
            await clbck.message.edit_text(text.menu, reply_markup=kb.operation)
        elif state.get('menu') == 'subscriptions':
            await clbck.message.edit_text(text.menu, reply_markup=kb.subscriptions)
    elif clbck.data in lst_period:
        state_period = await state.update_data(period=clbck.data)
        logging.info('period: %r', state_period)
        state = await state.get_data()
        logging.info('state: %r', state)
        if state.get('menu') == 'all records':
            text_report = excel_read(state_period.get('operation'), state_period.get('period'))
            await clbck.message.edit_text(text=text_report, reply_markup=kb.excel)
        elif state.get('menu') == 'subscriptions':
            text_report = subscriptions_data(state_period.get('operation'), state_period.get('period'))
            await clbck.message.edit_text(text=text_report, reply_markup=kb.excel)
    #
    # elif clbck.data == excel_button:
    #     state = await state.get_data()
    #     # logging.info('log_state: %r', state)
    #     file = uploads_excel(state['operation'], state['period'])
    #     await clbck.message.answer_document(caption='Файл готов! ', document=file)
    # chat_id = clbck.message.chat.id
    # logging.info('user_chat_id: %r', chat_id)


@router.callback_query(F.data.in_({'excel'}))
async def excel_file(clbck: CallbackQuery, state: FSMContext):
    state = await state.get_data()
    if state.get('menu') == 'all records':
        file = uploads_excel(state['operation'], state['period'])
        await clbck.message.answer_document(caption='Файл готов!', document=file)
    elif state.get('menu') == 'subscriptions':
        file = ''
        await clbck.message.answer_document(caption='Файл готов!', document=file)


@router.message(F.text)
async def no_text(msg: types.Message):
    await msg.answer('Нажимайте кнопочки!')
