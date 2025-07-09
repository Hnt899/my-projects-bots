# app/handlers.py
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import app.database.requests as rq
from datetime import datetime, timedelta
import asyncio
import app.keyboards as kb

router = Router()

class RegistrationStates(StatesGroup):
    waiting_for_gender = State()
    waiting_for_age = State()
    waiting_for_weight = State()
    waiting_for_diseases = State()
    confirm_data = State()

gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Мужской'), KeyboardButton(text='Женский')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

diseases_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Бессонница')],
        [KeyboardButton(text='Апноэ')],
        [KeyboardButton(text='Храп')],
        [KeyboardButton(text='Нет проблем')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

async def check_registration(message: Message) -> bool:
    user = await rq.get_user(message.from_user.id)
    return user and user.is_registered if user else False

@router.message(CommandStart())
async def cmd_start(message: Message):
    if not await check_registration(message):
        await message.answer(
            "Добро пожаловать в бота для улучшения сна! Пройдите регистрацию.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text='Начать регистрацию')]],
                resize_keyboard=True
            )
        )
    else:
        await message.answer(
            "Главное меню:",
            reply_markup=kb.main
        )

@router.message(F.text == 'Начать регистрацию')
async def start_registration(message: Message, state: FSMContext):
    await state.set_state(RegistrationStates.waiting_for_gender)
    await message.answer(
        "Укажите ваш пол:",
        reply_markup=gender_keyboard
    )

@router.message(RegistrationStates.waiting_for_gender)
async def process_gender(message: Message, state: FSMContext):
    if message.text not in ['Мужской', 'Женский']:
        await message.answer("Пожалуйста, выберите пол используя кнопки")
        return
    
    await state.update_data(gender='M' if message.text == 'Мужской' else 'F')
    await state.set_state(RegistrationStates.waiting_for_age)
    await message.answer(
        "Введите ваш возраст:",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(RegistrationStates.waiting_for_age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (1 <= int(message.text) <= 120):
        await message.answer("Пожалуйста, введите корректный возраст (1-120)")
        return
    
    await state.update_data(age=int(message.text))
    await state.set_state(RegistrationStates.waiting_for_weight)
    await message.answer("Введите ваш вес в кг (30-200):")

@router.message(RegistrationStates.waiting_for_weight)
async def process_weight(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (30 <= int(message.text) <= 200):
        await message.answer("Пожалуйста, введите корректный вес (30-200 кг)")
        return
    
    await state.update_data(weight=int(message.text))
    await state.set_state(RegistrationStates.waiting_for_diseases)
    await message.answer(
        "Есть ли у вас проблемы со сном?",
        reply_markup=diseases_keyboard
    )

@router.message(RegistrationStates.waiting_for_diseases)
async def process_diseases(message: Message, state: FSMContext):
    if message.text not in ['Бессонница', 'Апноэ', 'Храп', 'Нет проблем']:
        await message.answer("Пожалуйста, выберите вариант из предложенных")
        return
    
    user_data = await state.get_data()
    await state.update_data(diseases=message.text)
    
    sleep_hours = 7
    if user_data['weight'] < 60:
        sleep_hours = 8
    elif user_data['weight'] > 90:
        sleep_hours = 9
    
    if user_data['gender'] == 'F':
        sleep_hours += 0.5
    
    await message.answer(
        f"Проверьте ваши данные:\n"
        f"▪ Пол: {'Мужской' if user_data['gender'] == 'M' else 'Женский'}\n"
        f"▪ Возраст: {user_data['age']} лет\n"
        f"▪ Вес: {user_data['weight']} кг\n"
        f"▪ Проблемы со сном: {message.text}\n"
        f"▪ Рекомендуемое время сна: {sleep_hours} часов\n\n"
        f"Всё верно?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Да, всё верно')],
                [KeyboardButton(text='Начать регистрацию заново')]
            ],
            resize_keyboard=True
        )
    )
    await state.set_state(RegistrationStates.confirm_data)

@router.message(RegistrationStates.confirm_data)
async def confirm_data(message: Message, state: FSMContext):
    if message.text == 'Начать регистрацию заново':
        await state.clear()
        await start_registration(message, state)
        return
    
    user_data = await state.get_data()
    
    await rq.create_or_update_user(
        tg_id=message.from_user.id,
        gender=user_data['gender'],
        age=user_data['age'],
        weight=user_data['weight'],
        diseases=user_data['diseases']
    )
    
    await message.answer(
        "Регистрация завершена!",
        reply_markup=kb.main
    )
    await state.clear()

@router.message(F.text == 'Связаться с админом')
async def contact_admin(message: Message):
    if not await check_registration(message):
        await message.answer("Для доступа к функциям завершите регистрацию")
        return
    
    await message.answer(
        "Вы можете связаться с администратором:\n"
        "Telegram: @yougogi\n"  
        "Email: georgasss0@gmail.com",         
        reply_markup=kb.main
    )
    
@router.message(F.text == 'Видео для улучшения сна')
async def show_sleep_videos(message: Message):
    if not await check_registration(message):
        await message.answer("Для доступа к функциям завершите регистрацию")
        return

    categories = await rq.get_sleep_categories()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for category in categories:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}")]
        )
    
    await message.answer("Выберите категорию:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("category_"))
async def show_category_content(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    contents = await rq.get_sleep_content(category_id)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for content in contents:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=content.name, callback_data=f"content_{content.id}")]
        )
    
    await callback.message.answer("Выберите вариант:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("content_"))
async def show_content_details(callback: CallbackQuery):
    content_id = int(callback.data.split("_")[1])
    content = await rq.get_content(content_id)
    
    if content:
        await callback.message.answer(
            f"📺 {content.name}\n"
            f"📝 {content.description}\n"
            f"🎥 Ссылка: {content.video_link}"
        )
    else:
        await callback.message.answer("Контент не найден")
    
    await callback.answer()

@router.message(F.text == 'Виды сна')
async def show_sleep_types(message: Message):
    if not await check_registration(message):
        await message.answer("Для доступа к функциям завершите регистрацию")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Здоровый сон', callback_data='sleep_healthy')],
        [InlineKeyboardButton(text='Осознанные сны', callback_data='sleep_lucid')],
        [InlineKeyboardButton(text='Бифазный сон', callback_data='sleep_biphasic')],
        [InlineKeyboardButton(text='Полифазный сон', callback_data='sleep_polyphasic')],
        [InlineKeyboardButton(text='Повторяющиеся сны', callback_data='sleep_recurring')]
    ])
    await message.answer("Выберите тип сна:", reply_markup=keyboard)

@router.callback_query(F.data.startswith('sleep_'))
async def send_sleep_info(callback: CallbackQuery):
    sleep_type = callback.data.split('_')[1]
    info = ""
    
    if sleep_type == 'healthy':
        info = "Здоровый сон — это качественный отдых, который помогает восстановиться, сохранить иммунитет, концентрацию и хорошее настроение 💤 Чтобы его достичь, важно ложиться и вставать в одно и то же время ⏰ За час до сна лучше убрать гаджеты 📱, а в комнате создать тишину, темноту и прохладу 🌙 Не стоит переедать на ночь и пить кофе во второй половине дня ☕️ Лёгкая активность в течение дня улучшит сон, а вечерние ритуалы — чтение, душ или медитация — помогут расслабиться и легче заснуть 🛁📖"
    elif sleep_type == 'lucid':
        info = "Осознанные сны — это сны, в которых человек понимает, что спит, и может управлять событиями 🧠✨ Они развивают креативность и помогают исследовать подсознание. Чтобы их достичь, делай проверки реальности днём (смотри на руки, читай текст дважды) 🖐️📖, веди дневник сновидений ✍️, повторяй перед сном установку: «Я пойму, что сплю» 🌙 и пробуй технику WBTB — проснись за 5–6 часов до обычного времени, побудь немного бодрствующим и снова ложись 🛏️ Главное — практика и терпение 🌌"
    elif sleep_type == 'biphasic':
        info = "Бифазный сон — это режим, при котором человек спит дважды в течение суток 💤 Такой подход может помочь чувствовать себя бодрее и продуктивнее, если соблюдать чёткое расписание. Один из вариантов: основной сон с 00:00 до 04:30 и короткий дневной с 13:30 до 15:00 ⏰ В сумме это около 6 часов сна, разделённых на два этапа. Такой режим требует привыкания и не всем подходит, поэтому важно прислушиваться к своему самочувствию и сохранять регулярность."
    elif sleep_type == 'polyphasic':
        info = "Полифазный сон — это режим, при котором человек спит несколько раз в сутки короткими промежутками вместо одного длительного сна 💤 Такой подход может освободить больше времени для бодрствования ⏰, но требует строгой дисциплины и адаптации. Популярные режимы: Everyman — основной сон 3 часа ночью 🌙 + 3 короткие дремы по 20 минут днём 🛏️ (всего ~4 ч); Uberman — только 6 дрем по 20 минут каждые 4 часа 🕑 (итого 2 ч сна в сутки); Dymaxion — 4 дремы по 30 минут каждые 6 часов ⏳ (всего 2 ч сна); Segmented sleep — 2 равных отрезка по 3–4 часа с перерывом между ними 🕓. Такие режимы считаются экстремальными и подходят не всем. Важно следить за самочувствием и быть готовым к периоду адаптации 🌙."
    elif sleep_type == 'recurring':
        info = "Повторяющиеся сны — это сны, которые возникают несколько раз и могут иметь схожий сюжет, образы или темы 🧠💭 Они часто связаны с неразрешёнными эмоциями, стрессом или переживаниями в реальной жизни. Такие сны могут указывать на то, что нужно обратить внимание на определённые аспекты жизни, которые требуют изменений или осознания. Чтобы интерпретировать повторяющиеся сны, важно обратить внимание на эмоции, которые они вызывают, а также на символику и контекст сна 🌙 Например, если снится, что вы постоянно бегаете, это может означать стремление избежать проблемы или нерешённого вопроса 🏃‍♀️. Если повторяется тема падения, это может указывать на чувство потери контроля или страха перед неудачей 😨. Главное — понять, что именно эти сны пытаются вам сообщить, и работать с этими чувствами или ситуациями в реальной жизни."
    
    await callback.message.answer(info)
    await callback.answer()

@router.message(F.text == 'Ложусь спать')
async def good_night(message: Message):
    user = await rq.get_user(message.from_user.id)
    if not user:
        await message.answer("Сначала пройдите регистрацию")
        return
    
    # Расчет времени пробуждения
    sleep_hours = 7
    if user.weight < 60:
        sleep_hours = 8
    elif user.weight > 90:
        sleep_hours = 9
    
    if user.gender == 'F':
        sleep_hours += 0.5
    
    wake_up_time = (datetime.now() + timedelta(hours=sleep_hours)).strftime("%H:%M")
    
    await message.answer(
        f"Спокойной ночи! 😴\n"
        f"Рекомендуемое время сна: {sleep_hours} часов\n"
        f"Будильник установлен на {wake_up_time}\n"
        f"Хорошего отдыха!"
    )
    
    # Имитация будильника (можно заменить на реальный)
    await asyncio.sleep(sleep_hours * 3600)
    await message.answer("🔔 Время просыпаться! Доброе утро! ☀️")

@router.message(F.text == 'Какие есть команды')
async def show_commands(message: Message):
    commands = [
        "Доступные команды:",
        "Начать регистрацию — первый шаг к улучшению сна ✍️",
        "Какие есть команды - чтобы понять, что я умею рассказать ❓",
        "После регистрации:",
        "Видео для расслабления и улучшения сна — поможет заснуть быстрее и крепче 🎥",
        "Виды сна — узнай, что происходит с телом и мозгом ночью 🌙",
        "Связаться с админом - если нужна помощь или остались вопросы 🛠️",
        "Ложусь спать - чтобы я пожелал тебе доброй ночи и запомнил время сна 😴"
    ]
    await message.answer("\n".join(commands)) 