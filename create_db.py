import sqlite3
import telebot
token = ""
cs = telebot.TeleBot(token)

connection = sqlite3.connect("portfolio.db", check_same_thread=False)
cursor = connection.cursor()
@cs.message_handler(commands=['delete'])
def delete(message):
    name = message.from_user.username
    cursor.execute("DELETE FROM users WHERE name = ?", (name,))
    connection.commit()
    cs.reply_to(message, f" @{message.from_user.username} успешно удален из БД")
@cs.message_handler(commands=['user'])
def task(message):
    cursor.execute("SELECT * FROM users")  
    users = cursor.fetchall()     
    if not users:
        cs.reply_to(message, f"{message.from_user.username}, база данных пока пуста!")
        return
    response = ""
    for user in users:
        id = user[0]
        name = user[1]
        age = user[2]
        response += f"{id} | @{name} | {age} \n"
    cs.reply_to(message, response)
    connection.commit()
@cs.message_handler(commands=['start'])
def answer (message):
    b = message.from_user.username
    c = message.chat.id
    cursor.execute("SELECT name FROM users WHERE name = ? ", (b,))
    p = cursor.fetchone()
    if p is None:
        cursor.execute("INSERT INTO users (name, age) VALUES (?,?)" , (b,c))
        cs.reply_to(message, f" @{b},вы успешно добавлену в базу данных!")
    else:
        cs.reply_to(message, f" @{b}, вы уже есть в базе!")
    connection.commit()
@cs.message_handler(commands=['update'])
def update(message):
    name = message.from_user.username
    age = 16
    cursor.execute("UPDATE users SET age = ? WHERE name = ?", (age,name))
    connection.commit()
    cs.reply_to(message, f" Обновлено!")
@cs.message_handler(commands=['users'])
def users(message):
    cursor.execute("SELECT * FROM users ORDER BY age ASC")
    users = cursor.fetchall()
    cursor.execute("SELECT COUNT(id) FROM users")
    coun = cursor.fetchone()[0] 
    rep = ""
    for user in users:
        id = user[0]
        name = user[1]
        age = user[2]
        rep += f" {id} | {name} | {age}\n"
    cs.reply_to(message, f"Полный список юзеров отфильтрованный по возрастанию ID \nВсего {coun} пользователей: \n\n{rep}")
@cs.message_handler(commands=['find'])
def find(message):
    target = message.text.split()
    if len(target)<2:
        cs.reply_to(message, "Ошибка!")
        return
    targ = target[1]
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (f"%{targ}%",))
    b = cursor.fetchall()
    rep = ""
    if not b:
        cs.reply_to(message, f"Таких не найдено!")
    else:
        for user in b:
            id = user[0]
            name = user[1]
            age = user[2]
            rep += f" {id} | @{name} | {age}\n"
        cs.reply_to(message, f"Вот что нашлось: \n\n{rep}")
print("Satisfied!")
while True:
    try:
        print("Бот запущен...")
        cs.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Произошла ошибка связи: {e}")
        import time
        time.sleep(5)