from blocks import global_var as gv
import PySimpleGUI as sg
import os
import shutil
from blocks.querry_by import querry_by_id_delete
from blocks.preload import preload_db
def open_window_extra_files():  # windowed script thar searches extra gifs and jpgs files
    root_main = gv.getv('root_main')
    filename_extra_files = gv.getv('filename_extra_files')
    number_of_disks = len(gv.getv('arr_drives'))
    text = ''
    progressbar_extra_files = [[sg.ProgressBar(100, orientation='h', size=(51, 10), key='progressbar_extra_files')]]
    layout = [[sg.Text(text, key='extra_files')], [sg.Frame('Progress', layout=progressbar_extra_files)]]
    window = sg.Window("Extra files", layout)
    progress_bar_extra_files = window['progressbar_extra_files']
    while True:
        event, values = window.read(timeout=0.001)
        if event == sg.WIN_CLOSED:
            break
        number_of_entry = 0
        for i in range(1, number_of_disks + 1):
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                number_of_entry += 1
        extra_file = open(root_main + filename_extra_files, "w")
        cnt = 0
        for i in range(1, number_of_disks + 1):
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                cnt += 1
                for vdio in os.scandir(root + entry.name + '/posters/'):
                    if vdio.is_file():
                        if not os.path.exists(root + entry.name + '/' + vdio.name[:-4] + '.mp4'):
                            # os.remove(root + entry.name +'/posters/' + vdio.name)
                            extra_file.write(root + entry.name + '/posters/' + vdio.name + '\n')
                for vdio in os.scandir(root + entry.name + '/posters/gif/'):
                    if vdio.is_file():
                        if not os.path.exists(root + entry.name + '/' + vdio.name[:-4] + '.mp4'):
                            # os.remove(root + entry.name +'/posters/gif/' + vdio.name)
                            extra_file.write(root + entry.name + '/posters/gif/' + vdio.name + '\n')

                extra_file.write("checked: " + entry.name + '\n')
                window['extra_files'].update(str(int(cnt / number_of_entry * 100)) + ' %')
                progress_bar_extra_files.UpdateBar(int(cnt / number_of_entry * 100))
                window.refresh()
        extra_file.close()
        window['extra_files'].update('Finished')
        window.refresh()

        break
    window.close()

def open_window_remove_extra_files():  # a script that removes all the extra files in a special folder
    root_main = gv.getv('root_main')
    filename_extra_files = gv.getv('filename_extra_files')
    number_of_disks = len(gv.getv('arr_drives'))
    text = ''
    progressbar_extra_files = [[sg.ProgressBar(100, orientation='h', size=(51, 10), key='progressbar_extra_files')]]
    layout = [[sg.Text(text, key='extra_files')], [sg.Frame('Progress', layout=progressbar_extra_files)]]
    window = sg.Window("Remove extra files", layout)
    progress_bar_extra_files = window['progressbar_extra_files']
    while True:
        event, values = window.read(timeout=0.001)
        if event == sg.WIN_CLOSED:
            break
        try:
            if not os.path.exists(root_main + 'extra'):
                os.makedirs(root_main + 'extra')
        except OSError:
            print('Error: Creating directory of data - extra')
        number_of_entry = 0
        for i in range(1, number_of_disks + 1):
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                number_of_entry += 1
        extra_file = open(root_main + filename_extra_files, "w")
        cnt = 0
        for i in range(1, number_of_disks + 1):
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                cnt += 1
                for vdio in os.scandir(root + entry.name + '/posters/'):
                    if vdio.is_file():
                        if not os.path.exists(root + entry.name + '/' + vdio.name[:-4] + '.mp4'):
                            try:
                                if not os.path.exists(root_main + 'extra/' + entry.name):
                                    os.makedirs(root_main + 'extra/' + entry.name)
                            except OSError:
                                print('Error: Creating directory of data - extra')
                            try:
                                if not os.path.exists(root_main + 'extra/' + entry.name + '/posters'):
                                    os.makedirs(root_main + 'extra/' + entry.name + '/posters')
                            except OSError:
                                print('Error: Creating directory of data - extra')
                            shutil.move(root + entry.name + '/posters/' + vdio.name,
                                        root_main + 'extra/' + entry.name + '/posters/' + vdio.name)
                            extra_file.write(root + entry.name + '/posters/' + vdio.name + '\n')
                for vdio in os.scandir(root + entry.name + '/posters/gif/'):
                    if vdio.is_file():
                        if not os.path.exists(root + entry.name + '/' + vdio.name[:-4] + '.mp4'):
                            try:
                                if not os.path.exists(root_main + 'extra/' + entry.name):
                                    os.makedirs(root_main + 'extra/' + entry.name)
                            except OSError:
                                print('Error: Creating directory of data - extra')
                            try:
                                if not os.path.exists(root_main + 'extra/' + entry.name + '/posters'):
                                    os.makedirs(root_main + 'extra/' + entry.name + '/posters')
                            except OSError:
                                print('Error: Creating directory of data - extra')
                            try:
                                if not os.path.exists(root_main + 'extra/' + entry.name + '/posters/gif'):
                                    os.makedirs(root_main + 'extra/' + entry.name + '/posters/gif')
                            except OSError:
                                print('Error: Creating directory of data - extra')
                            shutil.move(root + entry.name + '/posters/gif/' + vdio.name,
                                        root_main + 'extra/' + entry.name + '/posters/gif/' + vdio.name)
                            extra_file.write(root + entry.name + '/posters/gif/' + vdio.name + '\n')

                extra_file.write("checked: " + entry.name + '\n')
                window['extra_files'].update(str(int(cnt / number_of_entry * 100)) + ' %')
                progress_bar_extra_files.UpdateBar(int(cnt / number_of_entry * 100))
                window.refresh()
        extra_file.close()
        window['extra_files'].update('Finished')
        window.refresh()

        break
    window.close()

def open_window_remove_extra_files_from_db():  # removes extra entires from db
    db_preloaded = preload_db()
    number_of_disks = len(gv.getv('arr_drives'))
    root_main = gv.getv('root_main')
    text = ''
    progressbar_extra_files = [[sg.ProgressBar(100, orientation='h', size=(51, 10), key='progressbar_extra_files')]]
    layout = [[sg.Text(text, key='extra_files')], [sg.Frame('Progress', layout=progressbar_extra_files)]]
    window = sg.Window("Extra files", layout)
    progress_bar_extra_files = window['progressbar_extra_files']
    while True:
        event, values = window.read(timeout=0.001)
        if event == sg.WIN_CLOSED:
            break
        arr_in_db = db_preloaded.copy()
        number_of_entry = 0
        for i in range(1, number_of_disks + 1):
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                number_of_entry += 1
        cnt = 0
        for i in range(1, number_of_disks + 1):
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                cnt += 1
                for vdio in os.scandir(root + entry.name + '/'):
                    if vdio.is_file():
                        len_db = len(arr_in_db)
                        needed_number = -1  # flag and counter
                        for j in range(len_db):
                            if arr_in_db[j]['id_entry'] == entry.name and arr_in_db[j]['id_video'] == vdio.name[:-4]:
                                needed_number = j
                                break
                        if needed_number != -1:
                            arr_in_db.pop(needed_number)

                window['extra_files'].update(
                    'Finding entires to delete in a db:' + str(int(cnt / number_of_entry * 100)) + ' %')
                progress_bar_extra_files.UpdateBar(int(cnt / number_of_entry * 100))
                window.refresh()
        len_db_left = len(arr_in_db)
        cnt1 = 0
        for i in range(len_db_left):
            cnt1 += 1
            querry_by_id_delete(arr_in_db[i]['id_entry'], arr_in_db[i]['id_video'])
            window['extra_files'].update('Deleting entires in a db:' + str(int(cnt1 / number_of_entry * 100)) + ' %')
            progress_bar_extra_files.UpdateBar(int(cnt1 / len_db_left * 100))
            window.refresh()
        window['extra_files'].update('Finished')
        window.refresh()

        break
    window.close()