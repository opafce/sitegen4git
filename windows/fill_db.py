from blocks import global_var as gv
import PySimpleGUI as sg
import pymysql
import os
from blocks.querry_by import querry_by_id, querry_by_id_duration_and_quality, querry_by_id_datetime
from blocks.preload import preload_db
def open_window_fill_db():  # updates db but in a windowed mode
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    from windows.rename import rename
    rename()
    text = ''
    progressbar_fill_db = [[sg.ProgressBar(100, orientation='h', size=(51, 10), key='progressbar_fill_db')]]
    layout = [[sg.Text(text, key='fill_db')], [sg.Frame('Progress', layout=progressbar_fill_db)]]
    window = sg.Window("Fill db", layout)
    progress_bar_fill_db = window['progressbar_fill_db']
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
        while True:
            flag_break = 0
            event, values = window.read(timeout=0.001)
            if event == sg.WIN_CLOSED:
                flag_break = 1
                break
            number_of_entry = 0
            for i in range(1, number_of_disks + 1):
                root = root_main + str(i) + '/' + str(i) + '/'
                for entry in os.scandir(root):
                    number_of_entry += 1
            cnt = 0
            sum_broken = 0
            db_preloaded = preload_db()
            for i in range(1, number_of_disks + 1):
                if flag_break:
                    break
                root = root_main + str(i) + '/' + str(i) + '/'
                for entry in os.scandir(root):
                    cnt += 1
                    event, values = window.read(timeout=0.001)
                    if event == sg.WIN_CLOSED:
                        flag_break = 1
                        break
                    for vdio in os.scandir(root + entry.name + '/'):
                        if vdio.is_file():
                            if flag_break:
                                break
                            filename = root + entry.name + '/' + vdio.name
                            query2 = querry_by_id(entry.name, vdio.name[:-4], db_preloaded)
                            if query2 != '':
                                cur.execute(query2)
                                con.commit()
                    window['fill_db'].update(str(int(cnt / number_of_entry * 33)) + ' %')
                    progress_bar_fill_db.UpdateBar(int(cnt / number_of_entry * 33))
                    window.refresh()
            db_preloaded = preload_db()

            for i in range(1, number_of_disks + 1):
                if flag_break:
                    break
                root = root_main + str(i) + '/' + str(i) + '/'
                for entry in os.scandir(root):
                    cnt += 1
                    event, values = window.read(timeout=0.001)
                    if event == sg.WIN_CLOSED:
                        flag_break = 1
                        break
                    if flag_break:
                        break
                    for vdio in os.scandir(root + entry.name + '/'):
                        if vdio.is_file():
                            if flag_break:
                                break
                            filename = root + entry.name + '/' + vdio.name
                            query3, query4 = querry_by_id_duration_and_quality(entry.name, vdio.name[:-4], filename, db_preloaded)
                            if query3 != '' or query4 != '':
                                if query3 != '':
                                    cur.execute(query3)
                                    con.commit()
                                if query4 != '':
                                    cur.execute(query4)
                                    con.commit()
                    window['fill_db'].update(str(int(cnt / number_of_entry * 33)) + ' %')
                    progress_bar_fill_db.UpdateBar(int(cnt / number_of_entry * 33))
                    window.refresh()
                db_preloaded = preload_db()

            for i in range(1, number_of_disks + 1):
                if flag_break:
                    break
                root = root_main + str(i) + '/' + str(i) + '/'
                for entry in os.scandir(root):
                    cnt += 1
                    event, values = window.read(timeout=0.001)
                    if event == sg.WIN_CLOSED:
                        flag_break = 1
                        break
                    if flag_break:
                        break
                    for vdio in os.scandir(root + entry.name + '/'):
                        if vdio.is_file():
                            if flag_break:
                                break
                            filename = root + entry.name + '/' + vdio.name
                            query5 = querry_by_id_datetime(entry.name, vdio.name[:-4], filename, db_preloaded)
                            if query5 != '':
                                cur.execute(query5)
                                con.commit()
                    window['fill_db'].update(str(int(cnt / number_of_entry * 33)) + ' %')
                    progress_bar_fill_db.UpdateBar(int(cnt / number_of_entry * 33))
                    window.refresh()
            window['fill_db'].update('Finished')
            window.refresh()

            break
    db_preloaded = preload_db()
    window.close()