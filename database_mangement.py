import sqlite3 as sql
from datetime import datetime


def insert_user(username, password, first_name, last_name, dob, gender):
    con = sql.connect('userData.db')
    cur = con.cursor()
    cur.execute("""
            INSERT INTO Users 
            (Username, Password, Created, First_Name, Last_Name, DOB, Gender)
            VALUES (?,?,?,?,?,?,?)""",
                (username, password, datetime.now(), first_name, last_name, dob, gender))
    con.commit()
    con.close()

def insert_drawing(id, name, user, data, canvas_image):
    con = sql.connect('userData.db')
    cur = con.cursor()
    cur.execute("""
                INSERT INTO Whiteboards
                (id, WBName, Username, Timestamp, data, canvas_image)
                VALUES (?,?,?,?,?,?)
                """,
                (id, name, user, datetime.now(), data, canvas_image))
    con.commit()
    con.close()

def get_all_users():
    con = sql.connect('userData.db')
    cur = con.cursor()
    cur.execute("""
    SELECT id, Username, Password FROM Users""")
    users = cur.fetchall()
    con.close()
    return users


def get_unique_user(username):
    con = sql.connect('userData.db')
    cur = con.cursor()
    cur.execute("""
        SELECT * FROM Users where Username = (?)""", (username,))
    user = cur.fetchall()
    con.close()
    return user


def get_unique_user_by_id(id):
    con = sql.connect('userData.db')
    cur = con.cursor()
    cur.execute("""
        SELECT * FROM Users where id = (?)""", (id,))
    user = cur.fetchall()
    con.close()
    return user

def update_user_by_id(id, pw, fn, ln, dob, gd):
    con = sql.connect('userData.db')
    cur = con.cursor()
    cur.execute("""
        UPDATE Users 
        SET Password = (?), 
        First_Name = (?), 
        Last_Name = (?),
        DOB = (?),
        Gender = (?)
        WHERE id = (?);""", (pw, fn, ln, dob, gd, id))
    con.commit()

