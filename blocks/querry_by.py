from blocks import global_var as gv
from blocks.utilities import get_video_duration, get_video_quality
import pymysql
import datetime
import os
def querry_by_id(id_entry, id_video, db_preloaded):  # returns a querry string for likes

    query2 = ''
    cnt = -1  # flag and counter
    len_db = len(db_preloaded)
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            cnt = i
            break

    if cnt == -1:
        anal = '0'
        like = '0'

        query2 = '''INSERT INTO categories (`id_entry`, `id_video`, `anal`, `likes`) VALUES ("''' + id_entry + '''","''' + id_video + '''","''' + anal + '''","''' + like + '''")'''
    return query2


def querry_by_id_delete(id_entry, id_video):  # returns a querry string for deleting extra strings from the db
    db_host = gv.getv('db_host')
    db_user = gv.getv('db_user')
    db_password = gv.getv('db_password')
    db_database = gv.getv('db_database')
    con = pymysql.connect(host=db_host,
                          user=db_user,
                          password=db_password,
                          database=db_database,
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
    with con:
        cur = con.cursor()
        query2 = '''DELETE FROM categories WHERE `id_video` = "''' + id_video + '''"AND `id_entry` = "''' + id_entry + '''"'''
        cur.execute(query2)
        con.commit()


def querry_by_id_duration_and_quality(id_entry, id_video,
                                      filename, db_preloaded):  # returns a querry string for duration and quality from the db
    len_db = len(db_preloaded)
    cnt = -1  # flag and counter
    query3 = ''
    query4 = ''
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            cnt = i
            break
    if cnt >= 0:
        if db_preloaded[cnt]['duration'] == 0 or db_preloaded[cnt]['quality'] == '':
            if db_preloaded[cnt]['duration'] == 0:
                duration = get_video_duration(filename)
                if duration == "warning":
                    print('      ******', filename)
                else:
                    query3 = '''UPDATE categories SET `duration` = "''' + str(
                        duration) + '''" WHERE `id_video` = "''' + id_video + '''" AND `id_entry` = "''' + id_entry + '''"'''
            if db_preloaded[cnt]['quality'] == '':
                quality = get_video_quality(filename)
                query4 = '''UPDATE categories SET `quality` = "''' + quality + '''" WHERE `id_video` = "''' + id_video + '''" AND `id_entry` = "''' + id_entry + '''"'''
    return query3, query4

def querry_by_id_datetime(id_entry, id_video, filename, db_preloaded):
    datetime.datetime.fromtimestamp(int(os.path.getctime(filename)))  # returns a querry string for datetime from the db
    len_db = len(db_preloaded)
    cnt = -1  # flag and counter
    query5 = ''
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            cnt = i
            break
    if cnt >= 0:
        if str(db_preloaded[cnt]['datetime']) == '0000-00-00 00:00:00':
            query5 = '''UPDATE categories SET `datetime` = "''' + str(datetime.fromtimestamp(int(os.path.getmtime(
                filename)))) + '''" WHERE `id_video` = "''' + id_video + '''" AND `id_entry` = "''' + id_entry + '''"'''
    return query5

