from aiogram import Router
from aiogram.types import Message   
from database.models import Medicines

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
    response_lines = []
    for med in medicines:
        line = (f"<b>савдо номи:</b>\n {med.trade_name}\n"
                f"<b>МНН:</b>\n {med.mnn}\n"
                f"<b>Ишлаб чиқарувчи:</b>\n {med.manufacturer}\n"
                f"<b>Шакл:</b>\n {med.form}\n"
                f"<b>Рўйхатдан ўтказиш рақами:</b>\n {med.registration_number}\n"
                f"<b>аптекадаги энг киммат нарх(НДС билан):</b>\n {med.price}\n"
                f"<b>Тарқатиш режими:</b>\n {med.dispensing_mode}\n"
                "-------------------------")
        response_lines.append(line)
    response_text = "\n".join(response_lines)
    await message.answer(response_text, parse_mode="HTML")
