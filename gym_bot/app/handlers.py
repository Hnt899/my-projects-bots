# тело проекта, тут происхлдит всё регистрация/общением с ботом ну короче вставить сюда пот токен и будет основным файлом проекта XD
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from io import BytesIO
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from data.nutrition import NUTRITION_PLANS
import app.keyboards as kb
import app.database.requests as rq
import os

router = Router()

class RegistrationStates(StatesGroup): #регистрация
    waiting_for_gender = State()
    waiting_for_height = State()
    waiting_for_weight = State()

gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Мужской'), KeyboardButton(text='Женский')] #кнопки пола
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

async def check_registration(message: Message) -> bool:
    user = await rq.get_user(message.from_user.id)
    return user and user.is_registered if user else False

@router.message(CommandStart()) #ловил старт
async def cmd_start(message: Message):
    if not await check_registration(message):
        await message.answer(
            "Добро пожаловать! Для начала работы необходимо пройти регистрацию.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text='Начать регистрацию')]], #кнопка
                resize_keyboard=True
            )
        )
    else:
        await message.answer(
            "Главное меню:",
            reply_markup=kb.main
        )

@router.message(F.text == 'Начать регистрацию') #ловим Начать регистрацию
async def start_registration(message: Message, state: FSMContext):
    await state.set_state(RegistrationStates.waiting_for_gender)
    await message.answer(
        "Укажите ваш пол:",
        reply_markup=gender_keyboard
    )

@router.message(RegistrationStates.waiting_for_gender) #используем RegistrationStates для удобства (пол)
async def process_gender(message: Message, state: FSMContext):
    if message.text not in ['Мужской', 'Женский']:
        await message.answer("Пожалуйста, выберите пол используя кнопки")
        return
    
    await state.update_data(gender='M' if message.text == 'Мужской' else 'F')
    await state.set_state(RegistrationStates.waiting_for_height)
    await message.answer(
        "Введите ваш рост в см (100-250):",
        reply_markup=ReplyKeyboardRemove() 
    )

@router.message(RegistrationStates.waiting_for_height) # используем RegistrationStates для удобства (рост)
async def process_height(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (100 <= int(message.text) <= 250):
        await message.answer("Пожалуйста, введите корректный рост (100-250 см)") #ошибка
        return
    
    await state.update_data(height=int(message.text))
    await state.set_state(RegistrationStates.waiting_for_weight)
    await message.answer("Введите ваш вес в кг (30-200):")

@router.message(RegistrationStates.waiting_for_weight) #используем RegistrationStates для удобства (вес)
async def process_weight(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (30 <= int(message.text) <= 200):
        await message.answer("Пожалуйста, введите корректный вес (30-200 кг)") #ошибка
        return
    
    #Вносим в бд
    user_data = await state.get_data()
    weight = int(message.text)
    
    await rq.create_or_update_user(
        tg_id=message.from_user.id,
        gender=user_data['gender'],
        height=user_data['height'],
        weight=weight
    )
    
    # Реализация рекомендаций
    recommendation = ""
    if weight < 60:
        recommendation = "🏆 Для вас отлично подойдут кросс-фит тренировки!"
    elif weight > 90:
        recommendation = "🏆 Вам рекомендуются тренировки в воде и full-body упражнения!"
    
    await message.answer(
        f"✅ Регистрация завершена!\n"
        f"▪ Пол: {'Мужской' if user_data['gender'] == 'M' else 'Женский'}\n"
        f"▪ Рост: {user_data['height']} см\n"
        f"▪ Вес: {weight} кг\n\n"
        f"{recommendation if recommendation else 'Вы можете выбрать любые тренировки!'}",
        reply_markup=kb.main
    )
    await state.clear()

@router.message(F.text == 'Какие есть команды')
async def show_commands(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "- Начать регистрацию\n"
        "- Какие есть команды\n"
        "После регистрации будут доступны:\n"
        "- Настройка Тренировок\n"
        "- Настройка питания\n"
        "- Связаться с админом"
    )

@router.message(F.text == 'Настройка Тренировок') # ловим Настройка Тренировок
async def workout_setup(message: Message):
    if not await check_registration(message):
        await message.answer("Для доступа к тренировкам завершите регистрацию") #ошибка
        return
    
    # включаем клаву выбора категорий
    categories = await rq.get_categories()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for category in categories:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}")]
        )
    
    await message.answer("Выберите категорию тренировки:", reply_markup=keyboard)

#ловим категорию
@router.callback_query(F.data.startswith("category_"))
async def show_category_workouts(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    workouts = await rq.get_workouts(category_id)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for workout in workouts:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=workout.name, callback_data=f"workout_{workout.id}")]
        )
    
    await callback.message.answer("Выберите упражнение:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("workout_"))
async def show_workout_details(callback: CallbackQuery):
    workout_id = int(callback.data.split("_")[1])
    workout = await rq.get_workout(workout_id)
    
    if workout:
        await callback.message.answer(
            f"🏋️ {workout.name}\n"
            f"📝 {workout.description}\n"
            f"🎥 Видео: {workout.videotraining}"
        )
    else:
        await callback.message.answer("Упражнение не найдено")
    
    await callback.answer()

#делаем так что если пользователь не зареган и нажимает на эти кнопки то будет ошибка(подобное делали выше только для настройка тренировок)
@router.message(F.text.in_(['Настройка питания', 'Связаться с админом']))
async def require_registration(message: Message):
    if not await check_registration(message):
        await message.answer(
            "Для доступа к этой функции необходимо завершить регистрацию.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text='Начать регистрацию')]],
                resize_keyboard=True
            )
        )
        #эти кнопки
    else:
        if message.text == 'Настройка питания':
            await message.answer("Раздел питания:", reply_markup=kb.nutrition_types)
        elif message.text == 'Связаться с админом':
            await message.answer("Контакт нашего комюнити менеджера @yougogi")

@router.message(F.text == 'Настройка питания')
async def nutrition_setup(message: Message):
    if not await check_registration(message):
        await message.answer("Для доступа к настройке питания завершите регистрацию")
        return
    
    await message.answer(
        "Выберите тип питания:",
        reply_markup=kb.nutrition_types
    )

@router.callback_query(F.data.startswith('nutrition_'))
async def send_nutrition_info(callback: CallbackQuery):
    plan_type = callback.data.split('_')[1]
    
    if plan_type not in NUTRITION_PLANS:  
        await callback.answer("Тип питания не найден") #ошибка
        return
    
    plan = NUTRITION_PLANS[plan_type]  
    
    try:
        await callback.message.answer(plan['description'])
        await callback.message.answer(plan['content'])
        await callback.answer()
    except Exception as e:
        print(f"Error: {e}")
        await callback.message.answer("Ошибка при отправке информации") #ошибка
    