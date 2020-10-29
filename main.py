import telebot
import logging
import databse, menu
import time, os
import send
import googlemaps
from telebot import types
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

bot = telebot.TeleBot('1352987252:AAGNPJ9nsO0RZHZKBp5aVHcXTEQu674Vwkw', threaded=False)
gmaps = googlemaps.Client(key='AIzaSyDRKl8OISk95iXz7H5ZIMeyA-Y0bZTcfrU')

@bot.message_handler(commands=['start'])
def start_message(message):
    chatid = message.chat.id
    username = message.chat.username
    message_text = databse.select_text_short('start_text')
    new_user = databse.check_new_user(chatid)
    if new_user == 'none':
        databse.create_user(chatid, username)
        bot.send_message(chatid, message_text, reply_markup=menu.home_menu)
    else:
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы', reply_markup=menu.home_menu)
    
@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        destination = gmaps.reverse_geocode((message.location.latitude, message.location.longitude))
        build_id = destination[0]['address_components'][0]['long_name']
        street = destination[0]['address_components'][1]['long_name']
        location_bs = str(street) + ' ' + str(build_id)
        databse.update_adr(message.chat.id, location_bs.replace('\'', ''))
        bot.send_message(message.chat.id, 'Введіть дату заправки', reply_markup=menu.order_step_three)
        bot.register_next_step_handler(message, open_time)

@bot.message_handler(content_types= ["photo"])
def verifyUser(message):
    order_data = databse.select_order_data(message.chat.id)[0]
    chatid = "*chatid:* " + str(order_data[0]) + "\n"
    item = "*товар:* " + str(order_data[1]) + "\n"
    address = "*доставка:* " + str(order_data[3]) + "\n"
    car_num = "*номер машини:* " + str(order_data[4]) + "\n"
    liter = "*літрів:* " + str(order_data[5]) + "\n"
    date = "*Час:* " + str(order_data[6]) + "\n"
    time = "*дата:* " + str(order_data[10]) + "\n"
    pay_metod = "*метод оплати:* " + str(order_data[7]) + "\n"
    phone_num = "*телефон:* " + str(order_data[8]) + "\n"
    address_s = "*адреса доставки:* " + str(order_data[9])  + "\n"
    admin_message = "*New order*" + "\n" + chatid + item + address + car_num + liter + date + time + pay_metod + phone_num + address_s
    send.send_email(admin_message)
    bot.send_message(message.chat.id, admin_message, parse_mode="Markdown")
    #admin
    text_admin = databse.select_text_short('text_admin')
    admin_list = databse.get_admin_list()
    for adimn in admin_list:
        bot.send_message(message.chat.id, text_admin, reply_markup=menu.home_menu)
        bot.forward_message(adimn, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Скриншот оплаты отправлен')

@bot.message_handler(func=lambda message: message.text == "Контакти")
def contact(message):
    contact_text = databse.get_contact()
    bot.send_message(message.chat.id, str(contact_text))

@bot.message_handler(func=lambda message: message.text == "Вимоги")
def requir(message):
    requir_text = databse.get_requir()
    bot.send_message(message.chat.id, str(requir_text))

@bot.message_handler(func=lambda message: message.text == "Ціна")
def price(message):
    price_text = databse.get_price()
    bot.send_message(message.chat.id, str(price_text))

@bot.message_handler(func=lambda message: message.text == "Відмінити")
def stop_order(message):
    databse.delete_basket(message.chat.id)
    bot.send_message(message.chat.id, 'Замовлення скасоване', reply_markup=menu.home_menu)

@bot.message_handler(func=lambda message: message.text == "Назад в меню")
def beck_home(message):
    bot.send_message(message.chat.id, 'Ви в головному меню', reply_markup=menu.home_menu)

@bot.message_handler(func=lambda message: message.text == "Заявка")
def start_order(message):
    databse.delete_basket(message.chat.id)
    chatid = message.chat.id
    bot.send_message(chatid, 'Виберіть паливо', reply_markup=menu.start_order_menu)

def open_time(message):
    date = message.text
    chatid = message.chat.id
    databse.update_time(chatid, date)
    menu.chatid = chatid
    bot.send_message(chatid, 'Виберіть час: ', reply_markup=menu.time_menu)
    bot.register_next_step_handler(message, order_three_step)

def order_five_step(message):
    chatid = message.chat.id
    liter = message.text
    databse.update_liter(chatid, liter)
    type_pal = str(databse.get_type_pal(chatid))
    price = databse.select_price(type_pal)
    print(type_pal, price)
    if str(liter).isdigit():
        message_prict = 'До сплати: ' + str(float(price) * float(liter)) 
        bot.send_message(chatid, message_prict)
    bot.send_message(chatid, 'Введіть спосіб оплати".', reply_markup=menu.pya_menu)

def order_four_step(message):
    print(message)
    chatid = message.chat.id
    car_num = str(message.text)
    databse.update_car(chatid, car_num)
    listr = str(databse.select_text_short('liter'))
    bot.send_message(chatid, listr, reply_markup=menu.stop_menu)
    bot.register_next_step_handler(message, order_five_step)

def order_three_step(message):
    newid = message.chat.id
    datetime_hour = datetime.now().time().strftime('%H')
    print(str(datetime_hour))
    date = str(message.text)
    days = str(databse.select_days(newid))
    print(days)
    if str(days) == 'Завтра':
        try:
            chatid = message.chat.id
            databse.update_date(chatid, date)
            bot.send_message(chatid, 'Введи номер авто: ', reply_markup=menu.stop_menu)
            bot.register_next_step_handler(message, order_four_step)
        except Exception as e:
            print(e)
    elif str(date) == '08:00-12:00' and str(datetime_hour) < str(12) and str(days) == 'Сьогодні':
        chatid = message.chat.id
        databse.update_date(chatid, date)
        bot.send_message(chatid, 'Введи номер авто: ', reply_markup=menu.stop_menu)
        bot.register_next_step_handler(message, order_four_step)
    elif str(date) == '12:00-16:00' and str(datetime_hour) < str(16) and str(days) == 'Сьогодні':
        chatid = message.chat.id
        databse.update_date(chatid, date)
        bot.send_message(chatid, 'Введи номер авто: ', reply_markup=menu.stop_menu)
        bot.register_next_step_handler(message, order_four_step)
    elif str(date) == '16:00-20:00' and str(datetime_hour) < str(20) and str(days) == 'Сьогодні':
        chatid = message.chat.id
        databse.update_date(chatid, date)
        bot.send_message(chatid, 'Введи номер авто: ', reply_markup=menu.stop_menu)
        bot.register_next_step_handler(message, order_four_step)
    else:
        bot.send_message(message.chat.id, 'Не актуальное время, когда доставить? ', reply_markup=menu.order_step_three)
        bot.register_next_step_handler(message, open_time)
        

def address_get(message):
    pass
    

def order_two_step(message):
    menu.chatid = message.chat.id
    location = str(message.text)
    databse.update_location(message.chat.id, location)
    if location == 'Доставка':
        bot.send_message(message.chat.id, 'Поділіться місцезнаходженням: ', reply_markup=menu.location_menu)
        #bot.register_next_step_handler(message, address_get)
    else:
        bot.send_message(message.chat.id, 'Самовивіз в розробці, Поділіться місцезнаходженням: ', reply_markup=menu.location_menu)
        #bot.register_next_step_handler(message, address_get)
        #databse.update_adr(message.chat.id, '-')
        #bot.send_message(message.chat.id, 'Введіть дату заправки', reply_markup=menu.order_step_three)
        #bot.register_next_step_handler(message, order_three_step)


order_list = ['Бензин', 'Дизель']
@bot.message_handler(func=lambda message: message.text in order_list)
def add_item(message):
    message_text = message.text
    if str(message_text) == 'Бензин':
        item = 'А95'
    elif str(message_text) == 'Дизель':
        item = 'ДП'
    databse.insert_basket(message.chat.id, item)
    bot.send_message(message.chat.id, 'Виберіть спосіб доставки', reply_markup=menu.order_step_two)
    bot.register_next_step_handler(message, order_two_step)

def end_order(message):
    phone = message.text
    pay_type = databse.get_pay_type(message.chat.id)
    if str(phone).isdigit() and len(str(phone)) > 8:
        databse.update_phone(message.chat.id, phone)
        #admin
        if str(pay_type) == 'Готівка':
            order_data = databse.select_order_data(message.chat.id)[0]
            chatid = "*chatid:* " + str(order_data[0]) + "\n"
            item = "*товар:* " + str(order_data[1]) + "\n"
            address = "*доставка:* " + str(order_data[3]) + "\n"
            car_num = "*номер машини:* " + str(order_data[4]) + "\n"
            liter = "*літрів:* " + str(order_data[5]) + "\n"
            date = "*Час:* " + str(order_data[6]) + "\n"
            time = "*дата:* " + str(order_data[10]) + "\n"
            pay_metod = "*метод оплати:* " + str(order_data[7]) + "\n"
            phone_num = "*телефон:* " + str(order_data[8]) + "\n"
            address_s = "*адреса доставки:* " + str(order_data[9])  + "\n"
            admin_message = "*New order*" + "\n" + chatid + item + address + car_num + liter + date + time + pay_metod + phone_num + address_s
            send.send_email(admin_message)
            bot.send_message(message.chat.id, admin_message, parse_mode="Markdown")
            #admin
            text_admin = databse.select_text_short('text_admin')
            bot.send_message(message.chat.id, text_admin, reply_markup=menu.home_menu)
        else:
            bot.send_message(message.chat.id, 'заказ буде оформлений після відправки скріншоту з оплатою', reply_markup=menu.home_menu)
    else:
        not_actual_phone = databse.select_text_short('not_act_ph')
        bot.send_message(message.chat.id, not_actual_phone)
        bot.register_next_step_handler(message, end_order)

list_pay_method = ['Готівка', 'Карта', 'Термінал']
@bot.message_handler(func=lambda message: message.text in list_pay_method)
def payment(message):
    message_text = message.text
    databse.update_pay(message.chat.id, message_text)
    user_msg = str(databse.get_pay_text())
    if message_text == 'Готівка':
        phone = databse.select_text_short('phone')
        bot.send_message(message.chat.id, phone, reply_markup=menu.home_menu)
        bot.register_next_step_handler(message, end_order)
    else:
        bot.send_message(message.chat.id, user_msg, reply_markup=menu.home_menu)
        bot.register_next_step_handler(message, end_order)

@bot.message_handler(func=lambda message: message.text == 'Відгуки')
def reviews(message):
    list_rv = databse.select_reviews()
    for review in list_rv:
        bot.send_message(message.chat.id, review, reply_markup=menu.reviews_menu)

def review_adding(message):
    review = message.text
    databse.insert_review(message.chat.id, message.chat.first_name, review)
    bot.send_message(message.chat.id, 'Відгук успішно доданий', reply_markup=menu.home_menu)

@bot.message_handler(func=lambda message: message.text == 'Додати відгук')
def add_rew(message):
    bot.send_message(message.chat.id, 'Текст відгуку: ')
    bot.register_next_step_handler(message, review_adding)

@bot.message_handler(func=lambda message: message.text == 'goap')
def start_admin(message):
    chatid = message.chat.id
    list_admin = databse.get_admin_list()
    if str(chatid) in list_admin:
        bot.send_message(message.chat.id, 'Панель администратора', reply_markup=menu.admin_menu)

@bot.message_handler(func=lambda message: message.text == 'chatid')
def get_chat_id(message):
    bot.send_message(message.chat.id, message.chat.id)

def to_ad_func(message):
    user_ch = message.text
    databse.to_admin(user_ch)
    bot.send_message(message.chat.id, 'Успішно')

@bot.message_handler(func=lambda message: message.text == 'Призначити адміном')
def to_admin(message):
    chatid = message.chat.id
    list_admin = databse.get_admin_list()
    if str(chatid) in list_admin:
        bot.send_message(message.chat.id, 'Введіть chatid користувача: ')
        bot.register_next_step_handler(message, to_ad_func)

@bot.message_handler(func=lambda message: message.text == 'Змінити тексти')
def etit_txt(message):
    chatid = message.chat.id
    list_admin = databse.get_admin_list()
    if str(chatid) in list_admin:
        list_text = databse.select_text()
        for text in list_text:
            edit_menu = types.InlineKeyboardMarkup()
            edit_menu.row(types.InlineKeyboardButton(text='Редагувати', callback_data='edit'))
            bot.send_message(message.chat.id, text, reply_markup=edit_menu)

def editr(message):
    new_text = message.text
    databse.update_text(databse.editor, new_text)
    bot.send_message(message.chat.id, 'Успішно замінено')

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'edit':
        databse.editor = call.message.text
        bot.send_message(call.message.chat.id, 'Введіть новий текст: ')
        bot.register_next_step_handler(call.message, editr)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)