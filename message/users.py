from aiogram import Router, F
from aiogram.types import Message, CallbackQuery   
from database.models import Medicines
from aiogram.fsm.context import FSMContext
from keyboards.inline_btns import search_results_btn

router = Router()

@router.message()
async def get_medicines(message: Message):
    if not message.text:
        await message.answer("Илтимос, қидирилаётган дори номини матн шаклида юборинг.")
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
        f"Dori nomi: {medicine.trade_name}\n"
        f"Dori MNN: {medicine.mnn}\n"
        f"Dori chiqairlish shakli: {medicine.form}\n"
        f"Dori ro'yhatdan o'tkazish raqami: {medicine.registration_number}\n"
        f"Dori davlati: {medicine.state}\n"
        f"Dorini dorixonada b   eirsh tartibi: {medicine.dispensing_mode}\n"
        f"Dorini farm guruhi: {medicine.farm_group}\n"
        f"Dorini ATX kod: {medicine.code_atx}\n",
        "-------------------------"
    )   
    await callback.answer()

@router.callback_query(F.data.startswith("analogs_"))
async def process_analogs_callback(callback: CallbackQuery, state: FSMContext):
    medicine_code_atx = int(callback.data.split("_")[1])
    medicines = await Medicines.filter(code_atx=medicine_code_atx)
    await callback.message.answer("Qidiruv natijalari:", reply_markup=search_results_btn(medicines))
    await callback.answer() 
