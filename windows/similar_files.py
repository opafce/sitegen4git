from blocks import global_var as gv
import os
import PySimpleGUI as sg
import numpy as np
import imgsim
import time
import cv2
from blocks.utilities import seconds_to_time
import subprocess
def open_window_similar_files():  # window script that finds similar videos by vectoring every image and finding the distance beetween each pair of pictures
    root_main = gv.getv('root_main')
    filename_similar_list_folder = gv.getv('filename_similar_list_folder')
    filename_similar_list = gv.getv('filename_similar_list')
    filename_similar_list_auto = gv.getv('filename_similar_list_auto')
    filename_similar_list_auto_folder = gv.getv('filename_similar_list_auto_folder')
    number_of_disks = len(gv.getv('arr_drives'))
    dist_max = gv.getv('dist_max')
    entry_list = []
    flag_prestart = 1
    flag_choose_all = 0
    flag_break_main = 0
    len_dist_arr = 101
    distance_arr = np.zeros(len_dist_arr)
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
            entry_list.append(entry.name)

    layout = [[sg.Text('Choose folder to check', size=(30, 1), justification='left')],
              [sg.Listbox(values=entry_list, select_mode='multiple', key='fac', size=(30, 30))],
              [sg.Button('choose'), sg.Button('choose_all')]]
    # Define Window
    win = sg.Window('Choose a folder to search for similar files', layout, resizable=True, finalize=True)
    # Read  values entered by user
    event, values = win.read()
    if event == sg.WIN_CLOSED:
        flag_prestart = 0
    if event == 'choose_all':
        flag_choose_all = 1
    # close first window
    win.close()
    # access the selected value in the list box and add them to a string
    flag_start = 0
    if flag_choose_all == 0:
        if flag_prestart == 1:
            strx = ""
            for val in values['fac']:
                strx = strx + " " + val
            str_split = strx[1:len(strx)].split(' ')
            layout = [[sg.Text('Your chosen folders are: ', size=(30, 1), justification='left')],
                      [sg.Listbox(values=str_split, select_mode='browse', key='fac', size=(30, 6))],
                      [sg.Button('start')],
                      [sg.Button('cancel')]]
            win = sg.Window('Similar files search confirmation', layout, resizable=True, finalize=True)
            while True:
                event, values = win.read()
                if event == sg.WIN_CLOSED or event == 'cancel':
                    break
                if event == 'start':
                    flag_start = 1
                    break
            win.close()
    else:
        if flag_prestart == 1:
            flag_start = 1

    if flag_start == 1:
        text = ''
        progressbar_similar_files_folder = [
            [sg.ProgressBar(100, orientation='h', size=(51, 10), key='progressbar_similar_files_folder')]]
        layout = [[sg.Text(text, key='similar_files_folder')],
                  [sg.Frame('Progress', layout=progressbar_similar_files_folder),
                   sg.Text('Est. time:', key='est_time')]]
        window = sg.Window("Similar files", layout)
        progress_bar_similar_files_folder = window['progressbar_similar_files_folder']
        if flag_choose_all == 0:
            similar_list = open(root_main + filename_similar_list_folder, "w")
            similar_list_auto = open(root_main + filename_similar_list_auto_folder, "w")
        else:
            similar_list = open(root_main + filename_similar_list, "w")
            similar_list_auto = open(root_main + filename_similar_list_auto, "w")
        while True:
            if flag_break_main:
                break
            event, values = window.read(timeout=0.001)
            if event == sg.WIN_CLOSED:
                flag_break_main = 1
                break
            if flag_choose_all == 0:
                number_of_entry = len(str_split)
            else:
                number_of_entry = 0
                for i in range(1, number_of_disks + 1):
                    root = root_main + str(i) + '/' + str(i) + '/'
                    for entry in os.scandir(root):
                        number_of_entry += 1
                str_split = []

            cnt_entry = 0
            window['similar_files_folder'].update('Starting comparisson')
            progress_bar_similar_files_folder.UpdateBar(0)
            window.refresh()
            window.refresh()

            number_of_video = 0
            number_of_video_arr = []
            number_of_video_arr_squares = []
            for i in range(1, number_of_disks + 1):
                root = root_main + str(i) + '/' + str(i) + '/'
                for entry in os.scandir(root):
                    if entry.name in str_split or flag_choose_all == 1:
                        number_of_video_for_entry = 0
                        for vdio in os.scandir(root + entry.name + '/'):
                            if vdio.is_file() and vdio.name[-4:] != '.ini':
                                number_of_video += 1
                                number_of_video_for_entry += 1
                        number_of_video_arr.append(number_of_video_for_entry)
                        number_of_video_arr_squares.append(
                            (number_of_video_for_entry + 1) * number_of_video_for_entry / 2)
            average_number_of_videos = sum(number_of_video_arr) / number_of_entry
            number_of_video_squares = sum(number_of_video_arr_squares)
            cnt_linear = 0
            cnt_quadratic = 0
            time_linear_per_video = 0.001
            time_quadratic_per_video = 0.0001
            for i in range(1, number_of_disks + 1):
                if flag_break_main:
                    break
                root = root_main + str(i) + '/' + str(i) + '/'
                for entry in os.scandir(root):
                    cnt_linear_tmp = 0
                    cnt_quadratic_tmp = 0
                    if flag_break_main:
                        break
                    if entry.name in str_split or flag_choose_all == 1:
                        cnt_entry += 1
                        pathp = root + entry.name
                        similar_list.write('---' + pathp + ' found:\n')
                        count = 0
                        for vdio in os.scandir(pathp + '/posters/'):
                            if vdio.is_file():
                                count += 1
                        names = ["" for x in range(count)]
                        vtr = imgsim.Vectorizer()
                        vectors = []
                        i = 0
                        window['similar_files_folder'].update('Started preprocessing: ' + entry.name + ' 0%')
                        window.refresh()
                        time_linear_start = time.time()

                        for vdio in os.scandir(pathp + '/posters/'):
                            if flag_break_main:
                                break
                            if vdio.is_file():
                                cnt_linear_tmp += 1
                                event, values = window.read(timeout=0.000001)
                                if event == sg.WIN_CLOSED:
                                    flag_break_main = 1
                                    break
                                names[i] = vdio.name
                                img0 = cv2.imread(pathp + '/posters/' + vdio.name[:-4] + '.jpg')
                                vec0 = vtr.vectorize(img0)
                                vectors.append(vec0)
                                i += 1
                                cnt_linear += 1
                                progress_bar_similar_files_folder.UpdateBar(int(cnt_linear / number_of_video * 100))
                                window['similar_files_folder'].update(
                                    'Started preprocessing: ' + entry.name + ' ' + str(
                                        int(100 * (cnt_linear_tmp) / number_of_video_arr[cnt_entry - 1])) + '%')
                                window['est_time'].update('Est. time:' + seconds_to_time(int(time_linear_per_video * (
                                            number_of_video - cnt_linear) + time_quadratic_per_video * (
                                                                                                         number_of_video_squares - cnt_quadratic))))
                                window.refresh()
                        if number_of_video_arr[cnt_entry - 1] > average_number_of_videos / 2:
                            time_linear_per_video = (time.time() - time_linear_start) / number_of_video_arr[
                                cnt_entry - 1]
                        window['similar_files_folder'].update('Ending preprocessing: ' + entry.name)
                        window.refresh()
                        vectors = np.asarray(vectors)
                        time_quadratic_start = time.time()
                        for i in range(count):
                            if flag_break_main:
                                break
                            event, values = window.read(timeout=0.000001)
                            if event == sg.WIN_CLOSED:
                                flag_break_main = 1
                                break
                            window['similar_files_folder'].update('Started comparing: ' + entry.name + ' ' + str(
                                int(100 * (cnt_quadratic_tmp) / (
                                            (number_of_video_arr[cnt_entry - 1] + 1) * number_of_video_arr[
                                        cnt_entry - 1] / 2))) + '%')
                            window.refresh()
                            for j in range(i + 1, count):
                                if flag_break_main:
                                    break
                                cnt_quadratic_tmp += 1
                                dist = imgsim.distance(vectors[i], vectors[j])
                                if dist < len_dist_arr:
                                    distance_arr[round(dist)] += 1
                                cnt_quadratic += 1
                                window['est_time'].update('Est. time:' + seconds_to_time(int(time_linear_per_video * (
                                            number_of_video - cnt_linear) + time_quadratic_per_video * (
                                                                                                         number_of_video_squares - cnt_quadratic))))
                                window.refresh()
                                if dist < dist_max:
                                    similar_list.write('    ' + names[i][:-4] + '\n    ' + names[j][
                                                                                           :-4] + "\n        distance =" + str(
                                        dist) + '\n\n\n')
                                    similar_list_auto.write(
                                        pathp + '***' + names[i][:-4] + '***' + names[j][:-4] + '***' + str(
                                            dist) + '\n')
                        if number_of_video_arr[cnt_entry - 1] > average_number_of_videos / 2:
                            time_quadratic_per_video = (time.time() - time_quadratic_start) / (
                                        (number_of_video_arr[cnt_entry - 1] + 1) * number_of_video_arr[
                                    cnt_entry - 1] / 2)
                        window['similar_files_folder'].update('Ending comparing: ' + entry.name)

                        window.refresh()
            window.close()
            break
        #little script to pop up the graph of squared distance frequency
        '''if flag_break_main == 0:
            matplotlib.use('TkAgg')
            fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
            t = np.arange(0, len_dist_arr, 1)
            fig.add_subplot(111).plot(t, distance_arr)

            layout = [[sg.Text('Distance plot')],
               [sg.Canvas(key='-CANVAS-')],
               [sg.Button('Ok')]]
            window1 = sg.Window('Distance plot', layout, size=(715, 500), finalize=True, element_justification='center', font='Helvetica 18')
            # add the plot to the window
            tkcanvas = draw_figure(window1['-CANVAS-'].TKCanvas, fig)
            event, values = window1.read()
            window1.close()'''

def open_window_similar_list_auto_check():  # opens pregenerated similar files in win explorer to check if they are similar
    root_main = gv.getv('root_main')
    root_explorer = gv.getv('root_explorer')
    filename_similar_list_auto = gv.getv('filename_similar_list_auto')
    filename_similar_list_auto_folder = gv.getv('filename_similar_list_auto_folder')

    folder_flag = 0
    breakflag = 0

    layout = [[sg.Text('Should we check all similar files?')], [sg.Button("Yes"), sg.Button("Specific")]]
    window = sg.Window("Similar list auto check", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            breakflag = 1
            break
        elif event == "Yes":
            break
        elif event == "Specific":
            folder_flag = 1
            break
    window.close()
    os.system("taskkill /im explorer.exe /F")
    reopen_explorer = subprocess.Popen(root_explorer)
    if breakflag == 0:
        if folder_flag == 0:
            filename_similar_list_auto_check = root_main + filename_similar_list_auto
        else:
            filename_similar_list_auto_check = root_main + filename_similar_list_auto_folder
        line_arr = []
        number_similar_files_checks = 0
        with open(filename_similar_list_auto_check) as f:
            for line in f:
                line_arr.append(line.strip())
                number_similar_files_checks += 1
        f.close()
        if number_similar_files_checks > 0:
            line_for_check = line_arr[0]
            line_for_check_br = line_for_check.split('***')
            local_path = line_for_check_br[0]
            path2 = local_path.replace(':', '%3A')
            path2 = path2.replace('/', '%5C')
            query_string1 = '''search-ms:displayname=Результаты%20поиска%20в%20"''' + local_path.split('/')[
                -1] + '''"&crumb=System.Generic.String%3A''' + line_for_check_br[1] + '''&crumb=location:''' + path2
            query_string2 = '''search-ms:displayname=Результаты%20поиска%20в%20"''' + local_path.split('/')[
                -1] + '''"&crumb=System.Generic.String%3A''' + line_for_check_br[2] + '''&crumb=location:''' + path2
            # if length > it doesnt work, i dont know how to fix it
            if len(query_string1) > 255:
                diff = len(query_string1) - 255
                query_string1 = '''search-ms:displayname=Результаты%20поиска%20в%20"''' + local_path.split('/')[
                    -1] + '''"&crumb=System.Generic.String%3A''' + line_for_check_br[1][
                                                                   :-diff] + '''&crumb=location:''' + path2
            if len(query_string2) > 255:
                diff = len(query_string2) - 255
                query_string2 = '''search-ms:displayname=Результаты%20поиска%20в%20"''' + local_path.split('/')[
                    -1] + '''"&crumb=System.Generic.String%3A''' + line_for_check_br[2][
                                                                   :-diff] + '''&crumb=location:''' + path2


            distance = line_for_check_br[3]
            # open first file search
            subprocess.Popen(f'explorer /root,"{query_string1}"')
            # open second file search
            subprocess.Popen(f'explorer /root,"{query_string2}"')
            if number_similar_files_checks == 1:
                layout = [[sg.Text(line_for_check_br[0].split('/')[-1] + ': ', key='info_similar_entry')],
                          [sg.Text(line_for_check_br[1], key='info_similar_video_1')],
                          [sg.Text(' vs ')],
                          [sg.Text(line_for_check_br[2], key='info_similar_video_2')],
                          [sg.Text('distance = ' + line_for_check_br[3], key='info_similar_distance')],
                          [sg.Button("finish", key='next_b'),
                           sg.Text('Left: ' + str(number_similar_files_checks - 1), key='left_pairs')]]
            else:
                layout = [[sg.Text(line_for_check_br[0].split('/')[-1] + ': ', key='info_similar_entry')],
                          [sg.Text(line_for_check_br[1], key='info_similar_video_1')],
                          [sg.Text(' vs ')],
                          [sg.Text(line_for_check_br[2], key='info_similar_video_2')],
                          [sg.Text('distance = ' + line_for_check_br[3], key='info_similar_distance')],
                          [sg.Button("next", key='next_b'),
                           sg.Text('Left: ' + str(number_similar_files_checks - 1), key='left_pairs')]]
            window = sg.Window("Similar list auto check", layout)
            cnt = 1

            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    break
                elif event == "next_b":
                    if cnt < number_similar_files_checks:
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
                        query_string2 = '''search-ms:displayname=Результаты%20поиска%20в%20"''' + local_path.split('/')[
                            -1] + '''"&crumb=System.Generic.String%3A''' + line_for_check_br[
                                            2] + '''&crumb=location:''' + path2
                        # if length > it doesnt work, i dont know how to fix it
                        if len(query_string1) > 255:
                            diff = len(query_string1) - 255
                            query_string1 = '''search-ms:displayname=Результаты%20поиска%20в%20"''' + \
                                            local_path.split('/')[-1] + '''"&crumb=System.Generic.String%3A''' + \
                                            line_for_check_br[1][:-diff] + '''&crumb=location:''' + path2
                        if len(query_string2) > 255:
                            diff = len(query_string2) - 255
                            query_string2 = '''search-ms:displayname=Результаты%20поиска%20в%20"''' + \
                                            local_path.split('/')[-1] + '''"&crumb=System.Generic.String%3A''' + \
                                            line_for_check_br[2][:-diff] + '''&crumb=location:''' + path2
                        if number_similar_files_checks - cnt == 1:
                            window.FindElement('next_b').Update('finish')
                            window.refresh()
                        distance = line_for_check_br[3]
                        window['info_similar_entry'].update(line_for_check_br[0].split('/')[-1] + ': ')
                        window['info_similar_video_1'].update(line_for_check_br[1])
                        window['info_similar_video_2'].update(line_for_check_br[2])
                        window['info_similar_distance'].update('distance = ' + line_for_check_br[3])
                        window['left_pairs'].update('Left: ' + str(-cnt - 1 + number_similar_files_checks))
                        window.refresh()
                        # open first file search
                        subprocess.Popen('explorer /root,"' + query_string1 + '"')
                        # open second file search
                        subprocess.Popen('explorer /root,"' + query_string2 + '"')
                        cnt += 1
                    else:
                        break

            os.system("taskkill /im explorer.exe /F")
            reopen_explorer = subprocess.Popen(root_explorer)
            window.close()