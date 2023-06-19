import PySimpleGUI as sg
from blocks import global_var as gv
import pymysql
import shutil
import os
from windows.fill_db import open_window_fill_db
from windows.extra_files import open_window_remove_extra_files_from_db

def not_checked_ios():  # returns two arrays with entry and video that are not checked on ios yet (encoding may be corrupted and viewed on pc and not on ios)
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
        query1 = '''SELECT * FROM categories WHERE `checked_ios` = 0'''
        cur = con.cursor()
        cur.execute(query1)
        rows = cur.fetchall()
        arr_id_entry = []
        arr_id_video = []
        if (len(rows)) == 0:
            return 0, 0
        else:
            for row in rows:
                arr_id_entry.append(row['id_entry'])
                arr_id_video.append(row['id_video'])

        return arr_id_entry, arr_id_video


def not_checked_ios_verify():  # makes not checked entires checked
    # Connect to the database
    arr_id_entry, arr_id_video = not_checked_ios()
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
        if len(arr_id_entry) > 0:
            for i in range(len(arr_id_entry)):
                query1 = '''UPDATE categories SET `checked_ios` = 1 WHERE `id_video` = "''' + arr_id_video[
                    i] + '''" AND `id_entry` = "''' + arr_id_entry[i] + '''"'''
                cur.execute(query1)
                con.commit()


def generate_check_broken_video_ios_new():  # generates videos 6 video per page to check if they can be viewed on ios
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    open_window_fill_db()
    open_window_remove_extra_files_from_db()
    file_front = open(root_main + "index_check.html", "w")
    arr_videos_html = []
    arr_tags_html = []
    n_video_per_page_ios = 6
    entry_name, vdio_name = not_checked_ios()
    shutil.rmtree(root_main + 'entries_check', ignore_errors=True)
    try:
        if not os.path.exists(root_main + 'entries_check'):
            os.makedirs(root_main + 'entries_check')
    except OSError:
        print('Error: Creating directory of data - check_ios')
    if len(entry_name) != 0 and len(vdio_name) != 0:
        disk_arr_new = []
        entry_name_n = []
        vdio_name_n = []
        for i in range(1, number_of_disks + 1):
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                for vdio in os.scandir(root + entry.name + '/'):
                    if vdio.is_file() and vdio.name[-4:] != '.ini':
                        for j in range(len(entry_name)):
                            if entry.name == entry_name[j] and vdio.name[:-4] == vdio_name[j]:
                                disk_arr_new.append(i)
                                entry_name_n.append(entry.name)
                                vdio_name_n.append(vdio.name[:-4])

        for i in range(len(entry_name)):
            arr_tags_html.append('''<p>''' + entry_name_n[i] + '/' + vdio_name_n[i] + '''</p><br/>\n''')
            arr_videos_html.append(
                '''<video src="../''' + str(disk_arr_new[i]) + '''/''' + str(disk_arr_new[i]) + '''/''' + entry_name_n[
                    i] + '''/''' + vdio_name_n[
                    i] + '''.mp4" controls width="300" height="150" poster = " ./white.jpg"></video><br/>\n''')

        file_front.write('''<a href="entries_check/''' + '0' + '''.html''' + '''">start</a><br/>\n''')
        file_front.write('''</body>\n</html>''')
        file_front.close()
        for i in range(len(arr_videos_html) // n_video_per_page_ios):
            file_vdio = open(root_main + 'entries_check/' + str(i) + '''.html''', "w", encoding="utf-8")
            file_vdio.write('''<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n''')
            for j in range(n_video_per_page_ios):
                file_vdio.write(arr_tags_html[i * n_video_per_page_ios + j])
                file_vdio.write(arr_videos_html[i * n_video_per_page_ios + j])
            file_vdio.write('''<br/><br/><br/><br/><a href="./''' + str(
                i + 1) + '''.html" style="color:orange;font-weight:bold;font-size: 100px">next</a><a style="color:black;font-weight:bold;font-size: 100px">    ''' + str(
                i + 1) + '/' + str(len(arr_videos_html) // n_video_per_page_ios + 1) + '''</a><br/>\n''')
            file_vdio.write('''</body>\n</html>''')
            file_vdio.close()
        i = len(arr_videos_html) // n_video_per_page_ios
        file_vdio = open(root_main + 'entries_check/' + str(i) + '''.html''', "w", encoding="utf-8")
        file_vdio.write('''<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n''')
        for j in range(len(arr_videos_html) % n_video_per_page_ios):
            file_vdio.write(arr_tags_html[(i) * n_video_per_page_ios + j])
            file_vdio.write(arr_videos_html[(i) * n_video_per_page_ios + j])
        file_vdio.write(
            '''<br/><br/><br/><br/><p style="color:black;font-weight:bold;font-size: 100px">       ''' + str(
                i + 1) + '/' + str(len(arr_videos_html) // n_video_per_page_ios + 1) + '''</p><br/>\n''')
        file_vdio.write('''</body>\n</html>''')
        file_vdio.close()

def open_window_check_ios(flag_checked=0):  # generates broken on ios video pages
    text = ''
    layout = [[sg.Text(text, key='check_ios')], ]
    window = sg.Window("Check_ios", layout)
    while True:
        event, values = window.read(timeout=0.001)
        if event == sg.WIN_CLOSED:
            break
        if flag_checked:
            not_checked_ios_verify()
        else:
            generate_check_broken_video_ios_new()
        window['check_ios'].update('Finished')
        window.refresh()

        break
    window.close()