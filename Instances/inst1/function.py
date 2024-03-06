import sqlite3 
from classes import *
import bcrypt

response = ResponseMessage()

#Adds user to database
def add_user_to_database(username, email, password, salt):
    conn = sqlite3.connect('database/main.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, email, password, salt) VALUES (?, ?, ?, ?)", (username, email, password, salt))
    conn.commit()
    conn.close()

def get_salt(user):
    conn = sqlite3.connect('database/main.db')
    cursor = conn.cursor()
    cursor.execute("SELECT salt FROM Users WHERE username = ?", (user,))
    u = cursor.fetchall()
    conn.commit()
    conn.close()
    return u

#Check if email and password match
def check_user(data: UserLoginSchema):
    conn = sqlite3.connect('database/main.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM Users WHERE username = ?", (data.user_name,))
    u = cursor.fetchall()
    conn.commit()
    conn.close()
    if len(u) == 1:
        return True
    return False

def check_user_total(username, password, salt):
    salt_byte = salt.encode("utf-8")
    pass_hash = bcrypt.hashpw(password.encode('utf-8'), salt_byte)
    conn = sqlite3.connect('database/main.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM Users WHERE username = ?", (username,))
    u = cursor.fetchall()
    conn.commit()
    conn.close()
    if u[0][0] == pass_hash.decode('utf-8'):
        return True
    else: 
        return False


#Check if the email is already used by someone
def check_email_already_used(email): 
    conn = sqlite3.connect('database/main.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users where email = ?", (email,))
    u = cursor.fetchall()
    conn.commit()
    conn.close()
    if len(u) == 1:
        return True
    return False

#Check if the username is already used by someone
def check_user_already_used(user):
    conn = sqlite3.connect('database/main.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (user,))
    u = cursor.fetchall()
    conn.commit()
    conn.close()
    if len(u) == 1:
        return True
    return False

#check who friends are
def check_friends(user):
    conn = sqlite3.connect('database/main.db')
    cursor = conn.cursor()
    cursor.execute("SELECT friends from FRIENDS where user = ?", (user,))
    u = cursor.fetchall()
    conn.commit()
    conn.close()
    return u

def convert_list_to_database_list(array):
    stringcheese = ""
    j = 0
    while j < len(array):
        stringcheese += " "
        stringcheese += array[j]
        j+=1
    return stringcheese


