from aiogram.utils.keyboard import ReplyKeyboardBuilder

admin_markup = ReplyKeyboardBuilder()
admin_markup.button(text="Excelни юклаш")
admin_markup.button(text="Базани кўриш")
admin_markup.button(text="Базани тозалаш")
admin_markup.adjust(1)
admin_markup = admin_markup.as_markup(resize_keyboard=True)

back_markup = ReplyKeyboardBuilder()
back_markup.button(text="Орқага")
back_markup = back_markup.adjust(1).as_markup(resize_keyboard=True)

confirm_markup = ReplyKeyboardBuilder() 
confirm_markup.button(text="Ҳа")
confirm_markup.button(text="Йўқ")
confirm_markup = confirm_markup.adjust(2).as_markup(resize_keyboard=True)