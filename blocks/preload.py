import pymysql
from blocks import global_var as gv
def preload_db():  # preloads the database
    # Connect to the database
    db_host = gv.getv('db_host')
    db_user  = gv.getv('db_user')
    db_password = gv.getv('db_password')
    db_database = gv.getv('db_database')
    con = pymysql.connect(host=db_host,
                          user=db_user,
                          password=db_password,
                          database=db_database,
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
    with con:
        query1 = '''SELECT * FROM categories'''
        cur = con.cursor()
        cur.execute(query1)
        rows = cur.fetchall()

        db_preloaded = rows
    return db_preloaded

def preload_db_delete():  # preloads the delete database
    # Connect to the database
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
        query1 = '''SELECT * FROM categories_delete'''
        cur = con.cursor()
        cur.execute(query1)
        rows = cur.fetchall()
        db_preloaded_delete = rows
    return db_preloaded_delete


