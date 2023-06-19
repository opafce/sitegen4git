from blocks import global_var as gv
import PySimpleGUI as sg
import os
from blocks.utilities import get_n_video, seconds_to_time
import time
from PIL import Image

def open_window_broken_files():  # windowed script thar searches broken gifs and jpgs files
    root_main = gv.getv('root_main')
    filename_broken_files = gv.getv('filename_broken_files')
    number_of_disks = len(gv.getv('arr_drives'))
    estimation_number2 = gv.getv('estimation_number2')
    progressbar_broken_files = [[sg.ProgressBar(100, orientation='h', size=(51, 10), key='progressbar_broken_files')]]
    layout = [[sg.Text(str(0) + ' %', key='broken_files')],
              [sg.Frame('Progress', layout=progressbar_broken_files), sg.Text('Est. time: ' + '1:00', key='time')]]
    window = sg.Window("Broken files", layout)
    progress_bar_broken_files = window['progressbar_broken_files']
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
        broken_file = open(root_main + filename_broken_files, "w")
        cnt = 0
        cnt_video = 0
        number_of_video = get_n_video()
        est_time_arr = []
        for i in range(estimation_number2):
            est_time_arr.append(3599)
        for i in range(1, number_of_disks + 1):
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                cnt += 1
                event, values = window.read(timeout=0.001)
                if event == sg.WIN_CLOSED:
                    flag_break = 1
                    break
                for vdio in os.scandir(root + entry.name + '/'):
                    if vdio.is_file():
                        cnt_video += 1
                        time_est_start = time.time()
                        if flag_break:
                            break
                        if os.path.exists(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif'):

                            if (os.path.getsize(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif') == 0):
                                broken_file.write(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif\n')
                            else:
                                img = Image.open(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif')
                                if (img.n_frames < 2):
                                    broken_file.write(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif\n')
                                img.close()
                        if os.path.exists(root + entry.name + '/posters/' + vdio.name[:-4] + '.jpg'):
                            if os.path.getsize(root + entry.name + '/posters/' + vdio.name[:-4] + '.jpg') == 0:
                                broken_file.write(root + entry.name + '/posters/' + vdio.name[:-4] + '.jpg\n')
                        for j in range(estimation_number2 - 1):
                            est_time_arr[j] = est_time_arr[j + 1]
                        est_time_arr[estimation_number2 - 1] = (number_of_video - cnt_video) * (
                                    -time_est_start + time.time())
                        window['time'].update(
                            'Time left: ' + seconds_to_time(sum(est_time_arr) / estimation_number2) + ' s')
                        window.refresh()
                broken_file.write("checked: " + entry.name + '\n')
                window['broken_files'].update(str(int(cnt / number_of_entry * 100)) + ' %')
                progress_bar_broken_files.UpdateBar(int(cnt / number_of_entry * 100))
                window.refresh()
        broken_file.close()
        window['broken_files'].update('Finished')
        window.refresh()
        break
    window.close()