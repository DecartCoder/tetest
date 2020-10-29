from telebot import types
from datetime import datetime, timedelta

chatid = ''

home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
home_menu.row('Заявка', 'Ціна')
home_menu.row('Відгуки', 'Вимоги', 'Контакти')

start_order_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_order_menu.row('Відмінити', 'Бензин', 'Дизель')

order_step_two = types.ReplyKeyboardMarkup(resize_keyboard=True)
order_step_two.row('Відмінити', 'Самовывоз', 'Доставка')

order_step_three = types.ReplyKeyboardMarkup(resize_keyboard=True)
text_button_today = 'Сьогодні ' + str(datetime.now().date())
text_button_tommorow = 'Завтра ' + str(datetime.now().date() + timedelta(days=1))
order_step_three.row('Відмінити', text_button_today, text_button_tommorow)

stop_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
stop_menu.row('Відмінити')

pya_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
pya_menu.row('Готівка', 'Карта', 'Термінал')
pya_menu.row('Відмінити')

reviews_menu =  types.ReplyKeyboardMarkup(resize_keyboard=True)
reviews_menu.row('Назад в меню', 'Додати відгук')

admin_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu.row('Призначити адміном')
admin_menu.row('Змінити тексти')
admin_menu.row('Назад в меню')

time_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
time_menu.row('08:00-12:00')
time_menu.row('12:00-16:00')
time_menu.row('16:00-20:00')

location_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
location_menu.row(types.KeyboardButton(text="Відправити місцезнаходження", request_location=True))
location_menu.row('Відмінити')