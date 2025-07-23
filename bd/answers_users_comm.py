import os
import psycopg2
from dotenv import load_dotenv

def connect_bd():
    load_dotenv()
    connect = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                               password=os.getenv("DB_PASSWORD"), host=os.getenv("HOST"), port=os.getenv("DB_PORT"))
    return connect

def create_answer_from_user(from_user_id, stars):
    connect = connect_bd()
    cur = connect.cursor()
    sql = f"INSERT INTO answers_users (from_user_id, place, stars) " \
            f"VALUES ({from_user_id}, 'no_adress', {stars}) RETURNING id;"
    cur.execute(sql)
    id_new_answ = cur.fetchone()[0]
    connect.commit()
    connect.close()
    return id_new_answ

def create_answer_data_bd(answers_users_id, text=None, voice_id=None, \
        photo_id=None, video_id=None, sticker_id=None, gif_id=None, \
        document_id=None, video_note_id=None, inline_mess=None):
    connect = connect_bd()
    cur = connect.cursor()
    if text:
        sql = f"INSERT INTO answers_data (answers_users_id, text) "\
        f"VALUES ({answers_users_id}, '{text}');"
    elif voice_id:
        sql = f"INSERT INTO answers_data (answers_users_id, voice_id) "\
        f"VALUES ({answers_users_id},  '{voice_id}');"
    elif photo_id:
        sql = f"INSERT INTO answers_data (answers_users_id, photo_id) "\
        f"VALUES ({answers_users_id},  '{photo_id}');"
    elif video_id:
        sql = f"INSERT INTO answers_data (answers_users_id, video_id) "\
        f"VALUES ({answers_users_id},  '{video_id}');"
    elif sticker_id:
        sql = f"INSERT INTO answers_data (answers_users_id, sticker_id) "\
        f"VALUES ({answers_users_id},  '{sticker_id}');"
    elif gif_id:
        sql = f"INSERT INTO answers_data (answers_users_id, gif_id) "\
        f"VALUES ({answers_users_id},  '{gif_id}');"
    elif document_id:
        sql = f"INSERT INTO answers_data (answers_users_id, document_id) "\
        f"VALUES ({answers_users_id},  '{document_id}');"
    elif video_note_id:
        sql = f"INSERT INTO answers_data (answers_users_id, video_note_id) "\
        f"VALUES ({answers_users_id},  '{video_note_id}');"
    elif inline_mess:
        sql = f"INSERT INTO answers_data (answers_users_id, inline_mess) "\
        f"VALUES ({answers_users_id},  '{inline_mess}');"
    cur.execute(sql)
    connect.commit()
    connect.close()

def get_data_answer_from_user(answ_id):
    connect = connect_bd()
    cur = connect.cursor()
    sql = f"SELECT text, voice_id, photo_id, video_id, sticker_id, gif_id, document_id, video_note_id FROM answers_data WHERE " \
        f"answers_users_id={answ_id} ORDER BY created_at;"
    cur.execute(sql)
    res = cur.fetchall()
    connect.commit()
    connect.close()
    list_res = []
    for data in res:
        dict_res = {}
        dict_res['text'] = data[0]
        dict_res['voice_id'] = data[1]
        dict_res['photo_id'] = data[2]
        dict_res['video_id'] = data[3]
        dict_res['sticker_id'] = data[4]
        dict_res['gif_id'] = data[5]
        dict_res['document_id'] = data[6]
        dict_res['video_note_id'] = data[7]
        list_res.append(dict_res)
    return list_res

def select_answer(answer_id):
    connect = connect_bd()
    cur = connect.cursor()
    sql = f"SELECT id, from_user_id, place, stars FROM answers_users WHERE id={answer_id};"
    cur.execute(sql)
    res = cur.fetchone()
    connect.commit()
    connect.close()
    res_dict = {}
    if res: 
        res_dict['id'] = res[0]
        res_dict['from_user_id'] = res[1]
        res_dict['place'] = res[2]
        res_dict['stars'] = res[3]
    return res_dict

if __name__ == '__main__':
    pass