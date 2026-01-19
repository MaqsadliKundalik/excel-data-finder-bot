from aiogram.utils.keyboard import InlineKeyboardBuilder    
from typing import List
from database.models import Medicines

def search_results_btn(results: List[Medicines]):
    inline_markup = InlineKeyboardBuilder()
    for med in results:
        inline_markup.button(text=med.trade_name, callback_data=f"med_{med.id}")
    inline_markup.adjust(1)
    inline_markup = inline_markup.as_markup() 
    return inline_markup    

def del_medicine_btn(med_id: int):
    inline_markup = InlineKeyboardBuilder()
    inline_markup.button(text="O'chirish", callback_data=f"del_{med_id}")
    inline_markup.adjust(1)
    return inline_markup.as_markup() 

def analogs_btn(med_code_atx: int):
    inline_markup = InlineKeyboardBuilder()
    inline_markup.button(text="Analoglari", callback_data=f"analogs_{med_code_atx}")
    inline_markup.adjust(1)
    return inline_markup.as_markup()