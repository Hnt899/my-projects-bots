
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher, types
from app.create_bot import bot
from app.db.dao_models import UserDAO
from app.db.models import User
from app.keyboards import kb_main
from app.stages.states import RegForm
from aiogram.filters import StateFilter, CommandStart, Command
from aiogram.methods import SetMyCommands

async def set_menu_commands(role):
    commands=[
        types.BotCommand(command="/start", description="начало работы"),
       ]
    await bot(SetMyCommands(commands=commands))
async def start(message: types.Message, state: FSMContext, ):
    if not message.from_user.username:
        await bot.send_message(message.from_user.id, "Приветствую! Это бот для компании Х, для начала заполни username в профиле телеграм!")
        return
    await state.clear()
    await bot.send_message(message.from_user.id, "Приветствую! Это бот для компанни Х")
    await start_func(message.from_user.id, state)
async def start_func(chat_id, state: FSMContext):
    await set_menu_commands(user.role)
    user:User = await UserDAO.get_one_or_none(chat_id=chat_id)
    if user is None:
        # Write to db or another any action
        await bot.send_message(chat_id, "Выбери тип пользователя", reply_markup=kb_main.user_type_kb())
    else:
        if user.role == "Новый":
            await bot.send_message(chat_id, "Дождись, пока администрация тебя подтвердит.")
        else:
            await bot.send_message(chat_id, "Выбери действие", reply_markup=await kb_main.head_kb(int(chat_id)))
            '''TODO суперадмин может создавать пользователей и назначать им роли'''
async def start_callbacks(call: types.CallbackQuery, state: FSMContext):
    data= await state.get_data()
    if call.data == 'stagestart_driver' or call.data == 'stagestart_logist' \
        or call.data == 'stagestart_director' or call.data == 'stagestart_another':
        
        if call.data == 'stagestart_director':
            await state.update_data(role = 'Руководитель')
        elif call.data == 'stagestart_another':
            await state.update_data(role = 'Новый')
        await call.message.edit_text("Введите ФИО")
        await state.set_state(RegForm.fio)
    elif call.data == 'stagestart_menu':
        await start_func(call.from_user.id, state)

def register_handlers_start(dp: Dispatcher):
    dp.message.register(start, CommandStart())

    dp.callback_query.register(start_callbacks, lambda c: c.data.startswith('stagestart'))

