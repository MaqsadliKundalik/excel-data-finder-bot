from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove   
from database.models import Medicines
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from keyboards.inline_btns import search_results_btn, analogs_btn


router = Router()

@router.message(Command("start"))
async def admin(message: Message):
    await message.answer("Ushbu bot sizga O'zbekistonda mavjud dori vositalari va ularning analoglari haqida ma'lumot beradi.\n\nBotdan foydalanish uchun dorining savdo nomini kiriting.", reply_markup=ReplyKeyboardRemove())

@router.message()
async def get_medicines(message: Message):
    if not message.text:
        await message.answer("Qidiruv uchun dorini nomini kiriting.")
        return  
    search_query = message.text.strip().lower()
    
    # Барча дориларни олиш ва қўлда қидириш
    all_medicines = await Medicines.all()
    medicines = []

    for med in all_medicines:
        if search_query in med.trade_name.lower():
            medicines.append(med)
            if len(medicines) >= 10:
                break
    
    if not medicines:
        await message.answer("Кечирасиз, ҳеч қандай мос дори топилмади.")
        return
    await message.answer("Qidiruv natijalari:", reply_markup=search_results_btn(medicines))

@router.callback_query(F.data.startswith("med_"))   
async def process_medicine_callback(callback: CallbackQuery, state: FSMContext):
    medicine_id = callback.data.split("_")[1]
    medicine = await Medicines.get(id=medicine_id)
    await callback.message.answer(
        f"<b>Dori nomi:</b> {medicine.trade_name}\n"
        f"<b>Dori MNN:</b> {medicine.mnn}\n"
        f"<b>Dori chiqairlish shakli:</b> {medicine.form}\n"
        f"<b>Dori ro'yhatdan o'tkazish raqami:</b> {medicine.registration_number}\n"
        f"<b>Dori davlati:</b> {medicine.state}\n"
        f"<b>Dorini dorixonada beirsh tartibi:</b> {medicine.dispensing_mode}\n"
        f"<b>Dorini farm guruhi:</b> {medicine.farm_group}\n"
        f"<b>Dorini ATX kod:</b> {medicine.code_atx}\n",
        reply_markup=analogs_btn(medicine.code_atx),
        parse_mode="HTML"
    )   
    await callback.answer()

@router.callback_query(F.data.startswith("analogs_"))
async def process_analogs_callback(callback: CallbackQuery, state: FSMContext):
    medicine_code_atx = callback.data.split("_")[1]
    medicines = await Medicines.filter(code_atx=medicine_code_atx)
    await callback.message.answer("Qidiruv natijalari:", reply_markup=search_results_btn(medicines))
    await callback.answer() 
