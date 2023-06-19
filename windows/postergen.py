from blocks import global_var as gv
import PySimpleGUI as sg
import subprocess
import time
import socket

from blocks.utilities import seconds_to_time, broken_and_raw_gif_remove
from blocks.utilities import get_preview_left_number, get_video_duration, get_number_of_frames_by_duration
from blocks.utilities import kill_postergen_processes
from windows.generate_task import generate_task
def open_window_postergen(jpg_gen_flag=2, gif_gen_flag=4):  # windowed scropt for generating posters
    kill_postergen_processes()
    from windows.rename import rename
    from windows.update_progress import update_progress
    pids_to_del_filename = gv.getv('pids_to_del_filename')
    cpu_per_filename = gv.getv('cpu_per_filename')
    number_of_programs_jpg = gv.getv('number_of_programs_jpg')
    number_of_programs_gif = gv.getv('number_of_programs_gif')
    IP = gv.getv('IP')
    # socket ports
    broken_and_raw_gif_remove()
    rename()
    update_progress()
    text_arr = ['' for i in range(number_of_programs_jpg + number_of_programs_gif)]
    left_arr = ['' for i in range(number_of_programs_jpg + number_of_programs_gif)]
    time_arr = ['' for i in range(number_of_programs_jpg + number_of_programs_gif)]
    saving_flag = [1 for i in range(number_of_programs_gif)]
    time_from_saving = [time.time() for i in range(number_of_programs_gif)]
    time_from_saving_const = 30
    time_multiplier_const = 0.3
    wait_saving_time = [time_from_saving_const for i in range(number_of_programs_gif)]
    flag_duration = [0 for i in range(number_of_programs_gif)]
    time_multiplier = [time_multiplier_const for i in range(number_of_programs_gif)]
    connection_flag_jpg = []
    connection_flag_gif = []
    for i in range(jpg_gen_flag):
        connection_flag_jpg.append(1)
    for i in range(jpg_gen_flag, gv.getv('number_of_programs_jpg')):
        connection_flag_jpg.append(0)
    for i in range(gif_gen_flag):
        connection_flag_gif.append(1)
    for i in range(gif_gen_flag, gv.getv('number_of_programs_gif')):
        connection_flag_gif.append(0)
    number_of_programs_jpg = jpg_gen_flag
    number_of_programs_gif = gif_gen_flag
    generate_task()
    connection_arr = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in range(number_of_programs_jpg + number_of_programs_gif)]
    processes_jpg = []
    processes_gif = []
    PORT_jpg = []
    PORT_gif = []
    port_start_jpg = gv.getv('port_start')
    port_start_gif = port_start_jpg + 200

    file_del_pids = open(pids_to_del_filename, "a")
    for i in range(number_of_programs_jpg):
        PORT_jpg.append(port_start_jpg + i)
    for i in range(number_of_programs_gif):
        PORT_gif.append(port_start_gif + i)
    for i in range(number_of_programs_jpg):
        processes_jpg.append(subprocess.Popen(['python', './postergen/jpggen.py', str(i), str(PORT_jpg[i])]))
        file_del_pids.write(str(processes_jpg[i].pid) + '\n')
    for i in range(number_of_programs_gif):
        processes_gif.append(subprocess.Popen(['python', './postergen/gifgen.py', str(i), str(PORT_gif[i])]))
        file_del_pids.write(str(processes_gif[i].pid) + '\n')
    file_del_pids.close()

    jpg_left, gif_left = get_preview_left_number()
    cpu_per_file = open(cpu_per_filename, "r")
    cpu_max_load = cpu_per_file.read(2)
    cpu_per_file.close()
    for i in range(number_of_programs_jpg):
        connection_arr[i].connect((IP, PORT_jpg[i]))
    for i in range(number_of_programs_gif):
        connection_arr[number_of_programs_jpg + i].connect((IP, PORT_gif[i]))
    progressbar_arr = []
    progressbar_key_arr = []
    for i in range(number_of_programs_jpg + number_of_programs_gif):
        progressbar_key_arr.append('progressbar' + str(i))
        progressbar_arr.append([[sg.ProgressBar(100, orientation = 'h', size = (51, 10), key = progressbar_key_arr[i])]])
    layout = [[sg.Text('Photo left : '), sg.Text(str(jpg_left), key = 'photo1')]]
    for i in range(number_of_programs_jpg):
        tmp_arr = []
        tmp_arr1 = []
        tmp_arr.append(sg.Text(text_arr[i], key = 'text' + str(i)))
        tmp_arr1.append(sg.Frame('jpg' + str(i + 1), layout = progressbar_arr[i]))
        tmp_arr1.append(sg.Text(left_arr[i], key = 'left' + str(i)))
        layout.append(tmp_arr)
        layout.append(tmp_arr1)
    layout.append([])
    layout.append([sg.Text('Gifs left : '), sg.Text(str(gif_left), key='gif1')])
    for i in range(number_of_programs_jpg, number_of_programs_jpg + number_of_programs_gif):
        tmp_arr = []
        tmp_arr1 = []
        tmp_arr.append(sg.Text(text_arr[i], key = 'text' + str(i)))
        tmp_arr1.append(sg.Frame('gif' + str(i - number_of_programs_jpg + 1), layout = progressbar_arr[i]))
        tmp_arr1.append(sg.Text(time_arr[i], key = 'time' + str(i)))
        tmp_arr1.append(sg.Text(left_arr[i], key = 'left' + str(i)))
        layout.append(tmp_arr)
        layout.append(tmp_arr1)
    layout.append([sg.Text('Cpu limit is set to:' + cpu_max_load + '%', key='cpu_max_limit'),
                   sg.Button("Change_cpu_max_limit")])
    window = sg.Window("Preview_gen", layout, default_element_size=(12, 1), resizable=True, finalize=True)
    progress_bar_arr = []
    for i in range(len(progressbar_key_arr)):
        progress_bar_arr.append(window[progressbar_key_arr[i]])
    time_update_quantity = time.time()

    break_on_wait_flag = 1
    while True:
        if break_on_wait_flag == 0:
            break
        event, values = window.read(timeout=0.001)
        if event == sg.WIN_CLOSED or (sum(connection_flag_jpg) + sum(connection_flag_gif)) == 0:
            for i in range(number_of_programs_jpg):
                if connection_flag_jpg[i]:
                    connection_arr[i].send("break".encode('utf8'))
                    connection_arr[i].close()
            for i in range(number_of_programs_gif):
                if connection_flag_gif[i]:
                    connection_arr[i + number_of_programs_jpg].send("break".encode('utf8'))
                    connection_arr[i + number_of_programs_jpg].close()
            break_on_wait_flag = 0
        else:
            if event == 'Change_cpu_max_limit':
                cpu_per_file = open(cpu_per_filename, "r")
                cpu_max_load = cpu_per_file.read(2)
                cpu_per_file.close()
                layout = [
                    [sg.Text('Choose cpu max load:')],
                    [sg.Text(cpu_max_load, key='cpu_max_load')],
                    [sg.Slider(range=(10, 90), default_value=cpu_max_load,
                               expand_x=True, enable_events=True,
                               orientation='horizontal', key='slider')],
                    [sg.Button('Save&exit')]]
                wind = sg.Window('Change cpu max limit', layout, size=(715, 150), resizable=True, finalize=True)
                while True:
                    event1, vals = wind.read()
                    if event1 == 'Save&exit':
                        cpu_per_file = open(cpu_per_filename, "w")
                        cpu_per_file.write(str(int(vals['slider'])))
                        cpu_per_file.close()
                        window['cpu_max_limit'].update('Cpu limit is set to:' + str(int(vals['slider'])) + '%')
                        wind.refresh()
                        break
                    if event1 == sg.WIN_CLOSED:
                        break
                    if event1 == 'slider':
                        wind['cpu_max_load'].update(int(vals['slider']))
                wind.close()



            for i in range(number_of_programs_jpg):
                if connection_flag_jpg[i]:
                    rd = connection_arr[i].recv(4096)  # receive buffer
                    input_str = rd.decode('utf8')  # decoding
                    a = input_str.split(str(PORT_jpg[i]))  # input str split
                    b = []
                    if len(a) > 2:  # if too much in a buffer
                        b = a[-2].split('***')
                    if len(a) == 2:
                        b = a[-1].split('***')
                    if len(b) == 3:  # normal mode
                        window['text' + str(i)].update(b[1])
                        window['left' + str(i)].update('Left: ' + str(int(b[2]) - 1))
                        jpg_left -= 1
                        window['photo1'].update(str(jpg_left))
                    elif len(b) == 2:  # sleeping, saving mode
                        if b[1] != 'break':
                            progress_bar_arr[i].UpdateBar(0)
                            window['text' + str(i)].update(b[1])
                    if '***break' in input_str:
                        connection_flag_jpg[i] = 0
                        window['text' + str(i)].update('Finished')
                    window.refresh()
            for i in range(number_of_programs_gif):
                if connection_flag_gif[i] and saving_flag[i]:

                    rd = connection_arr[i + number_of_programs_jpg].recv(4096)  # receive buffer
                    input_str = rd.decode('utf8')  # decoding
                    a = input_str.split(str(PORT_gif[i]))  # input str split
                    b = a[0].split('***')

                    if len(a) > 2:  # if too much in a buffer
                        b = a[-2].split('***')
                    if len(a) == 2:
                        b = a[-1].split('***')
                    if len(b) == 5:  # normal mode
                        progress_bar_arr[i + number_of_programs_jpg].UpdateBar(int(b[2].split('%')[0]))
                        window['text' + str(i + number_of_programs_jpg)].update(b[1])
                        window['time' + str(i + number_of_programs_jpg)].update(seconds_to_time(int(b[3])))
                        window['left' + str(i + number_of_programs_jpg)].update('Left: ' + str(int(b[4]) - 1))
                        if flag_duration[i]:  # calculation to wait some time for saving as when savinbg the server can not send any data
                            wait_saving_time[i] = get_video_duration(b[1]) / 60
                            flag_duration[i] = 0
                    elif len(b) == 2:  # sleping saving or finishing mode
                        if b[1] != 'break' and b[1] != ' -> saving':
                            progress_bar_arr[i + number_of_programs_jpg].UpdateBar(0)
                            window['text' + str(i + number_of_programs_jpg)].update(b[1])
                            gif_left -= 1
                            window['gif1'].update(str(gif_left))
                    if 'break' in input_str:
                        connection_flag_gif[i] = 0
                        window['text' + str(i + number_of_programs_jpg)].update('Finished')
                    if ' -> saving' in input_str:
                        saving_flag[i] = 0
                        time_from_saving[i] = time.time()
                        window['text' + str(i + number_of_programs_jpg)].update(' -> saving')
                        progress_bar_arr[i + number_of_programs_jpg].UpdateBar(100)
                        flag_duration[i] = 1
                    window.refresh()

                if (saving_flag[i] == 0) and (time.time() - time_from_saving[i] > get_number_of_frames_by_duration(
                    60 * wait_saving_time[i]) * time_multiplier[i]):
                    saving_flag[i] = 1
            if time.time() - time_update_quantity > 30:
                jpg_left, gif_left = get_preview_left_number()
                window['photo1'].update(str(jpg_left))
                window['gif1'].update(str(gif_left))
                window.refresh()
                update_progress()
                time_update_quantity = time.time()
    window.close()
    kill_postergen_processes()



