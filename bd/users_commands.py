from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

def connect_bd():
    load_dotenv()
    connect = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                               password=os.getenv("DB_PASSWORD"), host=os.getenv("HOST"), port=os.getenv("DB_PORT"))
    return connect

def create_user(id, first_name, user_name):
    connect = connect_bd()
    cur = connect.cursor()
    sql = f"INSERT INTO users (id, first_name, user_name) VALUES ({id}, '{first_name}', '{user_name}');"
    cur.execute(sql)
    connect.commit()
    connect.close()

def select_user(user_id):
    connect = connect_bd()
    cur = connect.cursor()
    sql = f"SELECT id, first_name, user_name, is_active " \
        f"FROM users WHERE id={user_id};"
    cur.execute(sql)
    user = cur.fetchall()
    connect.commit()
    connect.close()
    done_dict = {}
    for ell in user:
        done_dict = {}
        done_dict['id'] = ell[0]
        done_dict['first_name'] = ell[1]
        done_dict['user_name'] = ell[2]
        done_dict['is_active'] = ell[3]
    return done_dict

def make_active_user(user_id):
    connect = connect_bd()
    cur = connect.cursor()
    sql = f"UPDATE users SET is_active=TRUE WHERE id={user_id};"
    cur.execute(sql)
    connect.commit()
    connect.close()

def make_deactivate_user(user_id):
    connect = connect_bd()
    cur = connect.cursor()
    sql = f"UPDATE users SET is_active=FALSE WHERE id={user_id};"
    cur.execute(sql)
    connect.commit()
    connect.close()



if __name__ == '__main__':
    # make_finish_flow_user(354585871)
    pass