from sqlite3 import connect
import psycopg2
import os
from dotenv import load_dotenv

def connect_bd():
    load_dotenv()
    connect = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                               password=os.getenv("DB_PASSWORD"), host=os.getenv("HOST"), port=os.getenv("DB_PORT"))
    return connect

# def create_db():
#     connect = connect_bd()
#     cur = connect.cursor()
#     cur.execute(
#         f'CREATE DATABASE stolovaya_local;'
#     )
#     connect.commit()
#     connect.close()

def create_table_users():
    connect = connect_bd()
    cur = connect.cursor()
    cur.execute(
        f'CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY, ' \
        f'first_name VARCHAR(255), ' \
        f'user_name VARCHAR(255), ' \
        f'is_active BOOL DEFAULT TRUE, ' \
        f'created_at timestamp DEFAULT NOW());'
    )
    connect.commit()
    connect.close()

def create_table_answers_users():
    connect = connect_bd()
    cur = connect.cursor()
    cur.execute(
        f'CREATE TABLE IF NOT EXISTS answers_users (id SERIAL PRIMARY KEY, ' \
        f'from_user_id BIGINT REFERENCES users (id), ' \
        f'place VARCHAR(255), ' \
        f'stars INTEGER DEFAULT 0,'
        f'created_at timestamp DEFAULT NOW());'
    )
    connect.commit()
    connect.close()

def create_table_answers_data():
    connect = connect_bd()
    cur = connect.cursor()
    cur.execute(
        f'CREATE TABLE IF NOT EXISTS answers_data (id SERIAL PRIMARY KEY, ' \
        f'answers_users_id INTEGER REFERENCES answers_users (id), ' \
        f'text TEXT , ' \
        f'voice_id TEXT, ' \
        f'photo_id TEXT, ' \
        f'video_id TEXT, ' \
        f'sticker_id TEXT, ' \
        f'gif_id TEXT, ' \
        f'document_id TEXT, ' \
        f'video_note_id TEXT, ' \
        f'created_at timestamp DEFAULT NOW(), ' \
        f'updated_at timestamp DEFAULT NOW());'
    )
    connect.commit()
    connect.close()


def drop_table(name_table):
    connect = connect_bd()
    cur = connect.cursor()
    cur.execute(f'DROP TABLE "{name_table}" CASCADE')
    connect.commit()
    connect.close()

if __name__ == '__main__':
    # create_db()
    create_table_users()
    create_table_answers_users()
    create_table_answers_data()

    