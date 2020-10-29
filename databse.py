import sqlite3

conn = sqlite3.connect("palne.db")
cursor = conn.cursor()

editor = ''

def create_user(chatid, username):
    sql = 'insert into users(chatid, username)values(\'{0}\', \'{1}\');'.format(chatid, username)
    cursor.execute(sql)
    conn.commit()

def check_new_user(chatid):
    sql = 'select chatid from users where chatid = \'{0}\';'.format(chatid)
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    conn.commit()
    if result:
        return str(result[0][0])
    else:
        return 'none'

def get_contact():
    sql = 'select text from description_table where short_code = \'contact\';'
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    if result:
        return result[0][0]
    else:
        return None

def get_pay_text():
    sql = 'select text from description_table where short_code = \'pay_card\';'
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    if result:
        return result[0][0]
    else:
        return None

def get_requir():
    sql = 'select text from description_table where short_code = \'requir\';'
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    if result:
        return result[0][0]
    else:
        return None

def get_price():
    sql = 'select text from description_table where short_code = \'price\';'
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    if result:
        return result[0][0]
    else:
        return None

def insert_basket(chatid, item):
    sql = 'insert into basket(chatid, item)values(\'{0}\', \'{1}\');'.format(chatid, item)
    cursor.execute(sql)
    conn.commit()

def update_location(chatid, location):
    sql = 'update basket set delivery = \'{0}\' where chatid = \'{1}\';'.format(location, chatid)
    cursor.execute(sql)
    conn.commit()

def update_date(chatid, date):
    sql = 'update basket set date = \'{0}\' where chatid = \'{1}\';'.format(date, chatid)
    cursor.execute(sql)
    conn.commit()

def update_car(chatid, car):
    sql = 'update basket set car_num = \'{0}\' where chatid = \'{1}\';'.format(car, chatid)
    cursor.execute(sql)
    conn.commit()

def update_liter(chatid, liter):
    sql = 'update basket set liter = \'{0}\' where chatid = \'{1}\';'.format(liter, chatid)
    cursor.execute(sql)
    conn.commit()

def update_pay(chatid, pay):
    sql = 'update basket set pay_type = \'{0}\' where chatid = \'{1}\';'.format(pay, chatid)
    cursor.execute(sql)
    conn.commit()

def update_phone(chatid, phone):
    sql = 'update basket set client_phone = \'{0}\' where chatid = \'{1}\';'.format(phone, chatid)
    cursor.execute(sql)
    conn.commit()

def update_adr(chatid, adr):
    sql = 'update basket set city_address = \'{0}\' where chatid = \'{1}\';'.format(adr, chatid)
    cursor.execute(sql)
    conn.commit()

def update_time(chatid, time):
    sql = 'update basket set time = \'{0}\' where chatid = \'{1}\';'.format(time, chatid)
    cursor.execute(sql)
    conn.commit()

def delete_basket(chatid):
    sql = 'delete from basket where chatid = \'{0}\';'.format(chatid)
    cursor.execute(sql)
    conn.commit()

def select_order_data(chatid):
    sql = 'select * from basket where chatid = \'{0}\';'.format(chatid)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def select_reviews():
    sql = 'select text from reviews'
    cursor.execute(sql)
    result = cursor.fetchall()
    list_reviews = []
    for rv in result:
        list_reviews.append(rv[0])
    return list_reviews

def insert_review(chatid, name, text):
    sql = 'insert into reviews(chatid, username, text)values(\'{0}\', \'{1}\', \'{2}\');'.format(chatid, name, text)
    cursor.execute(sql)
    conn.commit()

def get_admin_list():
    sql = 'select chatid from users where admin = \'1\';'
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    list_admin = []
    for it in result:
        list_admin.append(it[0])
    return list_admin

def to_admin(chatid):
    sql = 'update users set admin = \'1\' where chatid = \'{0}\';'.format(chatid)
    cursor.execute(sql)
    conn.commit()

def select_text():
    sql = sql = 'select text from description_table;'
    cursor.execute(sql)
    result = cursor.fetchall()
    list_text = []
    for rz in result:
        list_text.append(rz[0])
    return list_text

def update_text(old_text, new_text):
    sql = 'update description_table set text = \'{0}\' where text = \'{1}\';'.format(new_text, old_text)
    cursor.execute(sql)
    conn.commit()

def select_text_short(short_code):
    sql = sql = 'select text from description_table where short_code = \'{0}\';'.format(short_code)
    cursor.execute(sql)
    result = cursor.fetchall()
    list_text = []
    for rz in result:
        list_text.append(rz[0])
    return list_text

def select_price(type_pal):
    sql = 'select price from product_list where name = \'{0}\';'.format(type_pal)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0][0]

def get_type_pal(chatid):
    sql = 'select item from basket where chatid = \'{0}\';'.format(chatid)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]
    
def select_days(chatid):
    sql = 'select time from basket where chatid = \'{0}\';'.format(chatid)
    cursor.execute(sql)
    result = cursor.fetchall()[0][0]
    conn.commit()
    data = str(result).split(' ')
    print(data)
    return data[0]

def get_pay_type(chatid):
    sql = 'select pay_type from basket where chatid = \'{0}\';'.format(chatid)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]