from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.models import Medicines
from utils.excel_saver import load_excel_to_database
from keyboards.reply_btns import admin_markup, back_markup, confirm_markup
from keyboards.inline_btns import search_results_btn, del_medicine_btn
from config import ADMIN_ID

from utils.states import AddMedicineState
from aiogram.filters import Command
from asyncio import sleep
import os
from aiogram.types import FSInputFile
    
router = Router()

@router.message(F.chat.id == ADMIN_ID, Command("start"))
async def f(message: Message, state: FSMContext):
    await message.answer(
        "Хуш келибсиз, админ! Қуйидаги тугмалардан бирини танланг:",
        reply_markup=admin_markup
    )

@router.message(F.chat.id == ADMIN_ID, F.text == "Ortga")
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ortga qaytdingiz!", reply_markup=admin_markup)

@router.message(F.chat.id == ADMIN_ID, F.text == "Dori qo'shish")
async def add_medicine(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Dori nomini kiriting:", reply_markup=back_markup)
    await state.set_state(AddMedicineState.trade_name)

@router.message(F.chat.id == ADMIN_ID, AddMedicineState.trade_name)
async def process_trade_name(message: Message, state: FSMContext):
    await state.update_data(trade_name=message.text)
    await message.answer("Dori MNN'sini kiriting:", reply_markup=back_markup)
    await state.set_state(AddMedicineState.mnn)

@router.message(F.chat.id == ADMIN_ID, AddMedicineState.mnn)
async def process_mnn(message: Message, state: FSMContext):
    await state.update_data(mnn=message.text)
    await message.answer("Dori chiqairlish shaklini kiriting:", reply_markup=back_markup)
    await state.set_state(AddMedicineState.form)



@router.message(F.chat.id == ADMIN_ID, AddMedicineState.form)
async def process_form(message: Message, state: FSMContext):
    await state.update_data(form=message.text)
    await message.answer("Dori ishlab chiqaruvchisini kiriting:", reply_markup=back_markup)
    await state.set_state(AddMedicineState.manufacturer)

@router.message(F.chat.id == ADMIN_ID, AddMedicineState.manufacturer)
async def process_manufacturer(message: Message, state: FSMContext):
    await state.update_data(manufacturer=message.text)
    await message.answer("Dori ro'yhatdan o'tkazish raqamini kiriting:", reply_markup=back_markup)
    await state.set_state(AddMedicineState.registration_number)

@router.message(F.chat.id == ADMIN_ID, AddMedicineState.registration_number)
async def process_registration_number(message: Message, state: FSMContext):
    await state.update_data(registration_number=message.text)
    await message.answer("Dori davlatini kiriting:", reply_markup=back_markup)
    await state.set_state(AddMedicineState.state)

@router.message(F.chat.id == ADMIN_ID, AddMedicineState.state)
async def process_state(message: Message, state: FSMContext):
    await state.update_data(state=message.text)
    await message.answer("Dorini dorixonada beirsh tartibini kiriting:", reply_markup=back_markup)
    await state.set_state(AddMedicineState.dispensing_mode)

@router.message(F.chat.id == ADMIN_ID, AddMedicineState.dispensing_mode)
async def process_dispensing_mode(message: Message, state: FSMContext):
    await state.update_data(dispensing_mode=message.text)
    await message.answer("Dorini farm guruhini kiriting:", reply_markup=back_markup)
    await state.set_state(AddMedicineState.farm_group)

@router.message(F.chat.id == ADMIN_ID, AddMedicineState.farm_group)
async def process_farm_group(message: Message, state: FSMContext):
    await state.update_data(farm_group=message.text)
    await message.answer("Dorini ATX kodini kiriting:", reply_markup=back_markup)
    await state.set_state(AddMedicineState.code_atx)

@router.message(F.chat.id == ADMIN_ID, AddMedicineState.code_atx)
async def process_code_atx(message: Message, state: FSMContext):
    await state.update_data(code_atx=message.text)
    data = await state.get_data()
    await message.answer(
        f"Ma'lumotlar:\n\n"
        f"Dori nomi: {data['trade_name']}\n"
        f"Dori MNN: {data['mnn']}\n"
        f"Dori chiqairlish shakli: {data['form']}\n"
        f"Dori ro'yhatdan o'tkazish raqami: {data['registration_number']}\n"
        f"Dori davlati: {data['state']}\n"
        f"Dorini dorixonada beirsh tartibi: {data['dispensing_mode']}\n"
        f"Dorini farm guruhi: {data['farm_group']}\n"
        f"Dorini ATX kod: {data['code_atx']}\n"
    )
    await message.answer("Dori qo'shishni tasdiqlaysizmi?", reply_markup=confirm_markup)
    await state.set_state(AddMedicineState.confirm)

@router.message(F.chat.id == ADMIN_ID, AddMedicineState.confirm)
async def process_confirm(message: Message, state: FSMContext):
    if message.text.lower() == "ha":
        data = await state.get_data()
        await Medicines.create(**data)
        await state.clear()
        await message.answer("Dori qo'shildi!", reply_markup=admin_markup)
    else:
        await state.clear()
        await message.answer("Dori qo'shilmadi!", reply_markup=admin_markup)

@router.message(F.chat.id == ADMIN_ID)
async def search_medicine(message: Message, state: FSMContext):
    q = message.text.strip().lower()
    
    results = []
    all_medicines = await Medicines.all()

    for med in all_medicines:
        if q in med.trade_name.lower():
            results.append(med)
            if len(results) >= 10:
                break
    
    if not results: 
        await message.answer("Кечирасиз, ҳеч қандай мос дори топилмади.")
        return
    
    markup = search_results_btn(results)
    await message.answer("Qidiruv natijalari:", reply_markup=markup)

@router.callback_query(F.chat.id == ADMIN_ID, F.data.startswith("med_"))
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
        parse_mode="HTML",
        reply_markup=del_medicine_btn(medicine_id)
    )

@router.callback_query(F.data.startswith("del_"))
async def process_delete_medicine_callback(callback: CallbackQuery, state: FSMContext):
    medicine_id = callback.data.split("_")[1]
    await Medicines.filter(id=medicine_id).delete()
    await callback.message.answer("Dori o'chirildi!")
    await callback.message.delete()
    