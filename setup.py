# creates database and tables for user data and saved whiteboards

import sqlite3

conn = sqlite3.connect('userData.db')

conn.execute(
    """
            CREATE TABLE IF NOT EXISTS Users(
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                Username VARCHAR(40) UNIQUE NOT NULL,
                Password VARCHAR(40) NOT NULL,
                Created DATETIME NOT NULL,
                First_Name VARCHAR(30) NOT NULL,
                Last_Name VARCHAR (30) NOT NULL,
                DOB DATE NOT NULL,
                Gender VARCHAR(25) NOT NULL
            )
    """
)

conn.execute(
    """
            CREATE TABLE IF NOT EXISTS Whiteboards(
                id     text PRIMARY KEY,
                WBName VARCHAR(40)NOT NULL,
                Username VARCHAR(40) NOT NULL,
                Timestamp DATETIME NOT NULL,
                data TEXT NOT NULL,
                canvas_image TEXT NOT NULL, 
                FOREIGN KEY (Username) REFERENCES Users(Username)
            )
    """
)
