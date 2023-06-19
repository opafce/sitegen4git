import subprocess
import os
from blocks import global_var as gv
import PySimpleGUI as sg
import pymysql
from blocks.preload import preload_db_delete
def delete_list_clear():  # empties the delete database
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
        query1 = '''DELETE FROM `categories_and_likes`.`categories_delete`'''
        cur = con.cursor()
        cur.execute(query1)
        con.commit()
def open_window_delete_list_auto_check():  # opens the files that where marked fot delete in db and one by one opens them in win explorer
    db_preloaded_delete = preload_db_delete()
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    root_explorer = gv.getv('root_explorer')
    filename_delete_list_auto = gv.getv('filename_delete_list_auto')

    line_arr = []
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
            for vdio in os.scandir(root + entry.name + '/'):
                if vdio.is_file() and vdio.name[-4:] != '.ini':
                    for row in db_preloaded_delete:
                        if row['id_entry'] == entry.name and row['id_video'] == vdio.name[:-4]:
                            line_arr.append(root + entry.name + '***' + vdio.name[:-4])
    breakflag = 0
    os.system("taskkill /im explorer.exe /F")
    reopen_explorer = subprocess.Popen(root_explorer)
    number_delete_files_checks = len(line_arr)
    if breakflag == 0:
        if number_delete_files_checks > 0:
            line_for_check = line_arr[0]
            line_for_check_br = line_for_check.split('***')
            local_path = line_for_check_br[0]
            path2 = local_path.replace(':', '%3A')
            path2 = path2.replace('/', '%5C')
            query_string1 = '''search-ms:displayname=Результаты%20поиска%20в%20"''' + local_path.split('/')[
                -1] + '''"&crumb=System.Generic.String%3A''' + line_for_check_br[1] + '''&crumb=location:''' + path2
            # if length > it doesnt work, i dont know how to fix it
            if len(query_string1) > 255:
                diff = len(query_string1) - 255
                query_string1 = '''search-ms:displayname=Результаты%20поиска%20в%20"''' + local_path.split('/')[
                    -1] + '''"&crumb=System.Generic.String%3A''' + line_for_check_br[1][
                                                                   :-diff] + '''&crumb=location:''' + path2
                # open file search
            subprocess.Popen(f'explorer /root,"{query_string1}"')
            if number_delete_files_checks == 1:
                layout = [[sg.Text(line_for_check_br[0].split('/')[-1] + ': ', key='info_delete_entry')],
                          [sg.Text(line_for_check_br[1], key='info_delete_video_1')],
                          [sg.Button("finish", key='next_b'),
                           sg.Text('Left: ' + str(number_delete_files_checks - 1), key='left_videos')]]
            else:
                layout = [[sg.Text(line_for_check_br[0].split('/')[-1] + ': ', key='info_delete_entry')],
                          [sg.Text(line_for_check_br[1], key='info_delete_video_1')],
                          [sg.Button("next", key='next_b'),
                           sg.Text('Left: ' + str(number_delete_files_checks - 1), key='left_videos')]]
            window = sg.Window("Delete list auto check", layout)
            cnt = 1
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    break
                elif event == "next_b":
                    if cnt < number_delete_files_checks:
                        os.system("taskkill /im explorer.exe /F")
                        reopen_explorer = subprocess.Popen(root_explorer)
                        line_for_check = line_arr[cnt]
                        line_for_check_br = line_for_check.split('***')
                        local_path = line_for_check_br[0]
                        path2 = local_path.replace(':', '%3A')
                        path2 = path2.replace('/', '%5C')
                        query_string1 = '''search-ms:displayname=Результаты%20поиска%20в%20"''' + local_path.split('/')[
                            -1] + '''"&crumb=System.Generic.String%3A''' + line_for_check_br[
                                            1] + '''&crumb=location:''' + path2
                        # if length > it doesnt work, i dont know how to fix it
                        if len(query_string1) > 255:
                            diff = len(query_string1) - 255
                            query_string1 = '''search-ms:displayname=Результаты%20поиска%20в%20"''' + \
                                            local_path.split('/')[-1] + '''"&crumb=System.Generic.String%3A''' + \
                                            line_for_check_br[1][:-diff] + '''&crumb=location:''' + path2
                        if number_delete_files_checks - cnt == 1:
                            window.FindElement('next_b').Update('finish')
                            window.refresh()
                        window['info_delete_entry'].update(line_for_check_br[0].split('/')[-1] + ': ')
                        window['info_delete_video_1'].update(line_for_check_br[1])
                        window['left_videos'].update('Left: ' + str(-cnt - 1 + number_delete_files_checks))
                        window.refresh()
                        # open file search
                        subprocess.Popen('explorer /root,"' + query_string1 + '"')
                        cnt += 1
                    else:
                        break
            os.system("taskkill /im explorer.exe /F")
            reopen_explorer = subprocess.Popen(root_explorer)
            window.close()