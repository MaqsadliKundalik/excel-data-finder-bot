from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.models import Medicines
from utils.excel_saver import load_excel_to_database
from keyboards.reply_btns import admin_markup, back_markup, confirm_markup
from config import ADMIN_ID
from utils.states import AdminStates
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


@router.message(F.chat.id == ADMIN_ID, F.text == "Орқага")
async def go_back(message: Message, state: FSMContext):
    await message.answer(
        "Асосий менюга қайтдингиз. Қуйидаги тугмалардан бирини танланг:",
        reply_markup=admin_markup
    )
    await state.clear()

@router.message(F.chat.id == ADMIN_ID, F.text == "Excelни юклаш")
async def upload_excel_prompt(message: Message, state: FSMContext):
    await message.answer(
        "Илтимос, Excel файлни юборинг (.xlsx форматда):",
        reply_markup=back_markup
    )
    await state.set_state(AdminStates.WAITING_FOR_EXCEL)

@router.message(F.chat.id == ADMIN_ID, AdminStates.WAITING_FOR_EXCEL)
async def handle_excel_upload(message: Message, state: FSMContext):
    if not message.document or not message.document.file_name.endswith('.xlsx'):
        await message.answer("Илтимос, фақат .xlsx форматдаги файлни юборинг.", reply_markup=back_markup)
        return

    file_info = await message.bot.get_file(message.document.file_id)
    downloaded_file = await message.bot.download_file(file_info.file_path)
    
    with open('data.xlsx', 'wb') as f:
        f.write(downloaded_file.read())

    progress_msg = await message.answer("⏳ Маълумотлар юкланмоқда... 0%")
    
    last_percent = 0
    
    async def update_progress(percent, current, total):
        nonlocal last_percent
        if percent >= last_percent + 10 or percent == 100:
            last_percent = percent
            progress_bar = "█" * (percent // 10) + "░" * (10 - percent // 10)
            await progress_msg.edit_text(
                f"⏳ Маълумотлар юкланмоқда...\n\n{progress_bar} {percent}%\n\n{current}/{total} қатор"
            )
    
    result = await load_excel_to_database('data.xlsx', update_progress)
    
    await progress_msg.delete()

    if result['success']:
        await message.answer(
            result['message'],
            reply_markup=admin_markup
        )
    else:
        await message.answer(
            f"Хатолик юз берди: {result['message']}",
            reply_markup=admin_markup
        )

    await state.clear()

@router.message(F.chat.id == ADMIN_ID, F.text == "Базани тозалаш")
async def confirm_clear_database(message: Message, state: FSMContext):
    await message.answer(
        "Ҳақиқатан ҳам базани тозаламоқчимисиз?",
        reply_markup=confirm_markup
    )
    await state.set_state(AdminStates.CONFIRM_CLEAR_DATABASE)

@router.message(F.chat.id == ADMIN_ID, AdminStates.CONFIRM_CLEAR_DATABASE, F.text == "Ҳа")
async def clear_database(message: Message, state: FSMContext):
    deleted_count = await Medicines.all().delete()
    
    # data.xlsx faylini o'chirish
    import os
    if os.path.exists('data.xlsx'):
        os.remove('data.xlsx')
    
    await message.answer(
        f"База тозаланди. {deleted_count} та ёзув ўчирилди.",
        reply_markup=admin_markup
    )
    await state.clear()

@router.message(F.chat.id == ADMIN_ID, AdminStates.CONFIRM_CLEAR_DATABASE, F.text == "Йўқ")
async def cancel_clear_database(message: Message, state: FSMContext):
    await message.answer(
        "База тозалаш бекор қилинди.",
        reply_markup=admin_markup
    )
    await state.clear()

@router.message(F.chat.id == ADMIN_ID, F.text == "Базани кўриш")
async def view_database(message: Message, state: FSMContext):
    import os
    from aiogram.types import FSInputFile
    
    # Bazada ma'lumot borligini tekshirish
    medicines_count = await Medicines.all().count()
    
    if medicines_count == 0:
        await message.answer(
            "📭 Базада ҳеч қандай маълумот йўқ.\n\nИлтимос, аввал Excel файлни юкланг.",
            reply_markup=admin_markup
        )
    elif os.path.exists('data.xlsx'):
        file = FSInputFile('data.xlsx')
        await message.answer_document(
            document=file,
            caption="📊 data.xlsx файли",
            reply_markup=admin_markup
        )
    else:
        await message.answer(
            "⚠️ data.xlsx файли топилмади. Илтимос, аввал Excel файлни юкланг.",
            reply_markup=admin_markup
        )
    
    await state.clear()