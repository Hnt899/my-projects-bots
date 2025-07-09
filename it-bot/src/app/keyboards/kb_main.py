from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.db.dao_models import UserDAO
from app.db.models import User
import math

async def head_kb(chat_id : int):
    # TODO There is the first MAIN keyboard, you need update it. U can it do according the role
    role = (await UserDAO.get_one_or_none(chat_id=chat_id)).role 
    kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[])
    if role == 'Role2':
        kb.inline_keyboard = [
            [InlineKeyboardButton(text='Item 1', callback_data=f'stage_routes')],
            [InlineKeyboardButton(text='Item 2', callback_data='stage_salary')],
        ]
        return kb

    
    if role == 'Суперадмин':
        kb.inline_keyboard.append(
            [InlineKeyboardButton(text='Руководители', callback_data=f'stageadmin_users_directors')])
    if role == 'Руководитель' or role == 'Суперадмин':
        kb.inline_keyboard.extend(
            [[InlineKeyboardButton(text='Role 1', callback_data=f'stageadmin_users_role1')],
            [InlineKeyboardButton(text='Новые пользователи', callback_data=f'stageadmin_users_another')]
            ])
        kb.inline_keyboard.append([InlineKeyboardButton(text='Статистика', callback_data='stageadmin_stats')])
    
    kb.inline_keyboard.append([InlineKeyboardButton(text='Водители', callback_data=f'stageadmin_users_drivers_0')])
    if role == 'Role 1' or role == 'Суперадмин':
        kb.inline_keyboard.extend(
            [[InlineKeyboardButton(text='Ставки', callback_data=f'stagelogist_rates')],
            ]
            )

    return kb



def user_list_kb(users: list[User], rrole, page: int = 0, quantity: int = 5):
    # TODO There is a sample kb with paged list
    kb = InlineKeyboardMarkup( inline_keyboard=[])

    for i in range(page*quantity, (page+1)*quantity if len(users)>(page+1)*quantity else len(users)):
        kb.inline_keyboard.append([InlineKeyboardButton(text=f"{users[i].username}", callback_data=f'stageadmin_profile_{rrole}_{page}_{users[i].id}')])
    tofrom = [] 
    if page == 0 and page < math.floor(len(users)/quantity):
        tofrom.append(InlineKeyboardButton(text="➡️", callback_data=f'stageadmin_users_{rrole}_{page+1}'))
    if page!= 0:
        tofrom.append(InlineKeyboardButton(text="⬅️", callback_data=f'stageadmin_users_{rrole}_{page-1}'))
    back = [InlineKeyboardButton(text="Назад", callback_data=f'stagestart_menu')]
    kb.inline_keyboard.append(tofrom)
    kb.inline_keyboard.append(back)
    return kb

def user_profile_kb(watcher: User, user: User,page, rrole):
    kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[])
    if user is None:
        kb.inline_keyboard.append(
        [InlineKeyboardButton(text='Назад', callback_data=f'stageadmin_users_{rrole}_{page}')])
        return kb
    # TODO here there are necessary buttons
    kb.inline_keyboard.append(
        [InlineKeyboardButton(text='Назад', callback_data=f'stageadmin_users_{rrole}_{page}')])
    
    return kb

def cancel_kb():
    # TODO make cancel Callback
    kb = InlineKeyboardMarkup( inline_keyboard=[])
    kb.inline_keyboard.append(
        [InlineKeyboardButton(text='Отмена', callback_data=f'stageadmin_cancel')])
    return kb

