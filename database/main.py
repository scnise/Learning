import telebot
import database as db
import time
token="8590528341:AAF9Cb1RADNOWPqPo49QOBWe8I6nlAck2kA"
cs = telebot.TeleBot(token)
db.init()
@cs.message_handler(commands =['start'])
def start(message):
    name = message.from_user.username
    id = message.chat.id
    s = db.adding(name,id)
    if s:
        cs.reply_to(message, f" @{name} вы успешно добавлены")
    else:
        cs.reply_to(message, f" @{name} вы уже есть в БД!")
@cs.message_handler(commands =['users'])
def adding(message):
    users = db.show()
    if not users:
        cs.reply_to(message, "Ошибка!")
        return
    response=""
    for user in users:
        id = user[0]
        name = user[1]
        age = user[2]
        response += f" {id} | @{name} | {age}\n"
    cs.reply_to(message, f"Вот полный список юзеров бота: \n\n{response}")
@cs.message_handler(commands =['del'])
def deleting(message):
    username = message.from_user.username
    db.delete(username)
@cs.message_handler(commands =['find'])
def find(message):
    b = message.text.split()
    if len(b)<2:
        cs.reply_to(message, "Неправильный формат, /find [name]")
        return
    c = b[1]
    t = db.find(f"%{c}%")
    response = ""
    if not t:
        cs.reply_to(message, f"Ошибка! В БД не найдено пользователей с юзернеймом {c}")
        return
    else:
        for user in t:
            id = user[0]
            name = user[1]
            age = user[2]
            response += f"{id} | {name} | {age}\n"
    cs.reply_to(message, response)
while True:
    try:
        cs.polling(none_stop=True)
        print("Succses!")
    except:
        time.sleep(5)
