import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nakul2803",   # ⚠️ CHANGE THIS
        database="movie_booking"
    )