from blocks import global_var as gv
import os
import PySimpleGUI as sg

def generate_task_old():  # generates a single task file
    root_main = gv.getv('root_main')
    filename_jpg_task = gv.getv('filename_jpg_task')
    filename_gif_task = gv.getv('filename_gif_task')
    number_of_disks = len(gv.getv('arr_drives'))
    jpg_task = open(root_main + filename_jpg_task, "w")
    gif_task = open(root_main + filename_gif_task, "w")
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
            for vdio in os.scandir(root + entry.name + '/'):
                if vdio.is_file() and vdio.name[-4:] != '.ini':
                    if not os.path.exists(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif'):
                        gif_task.write(root + entry.name + '\n')
                        gif_task.write(vdio.name + '\n')
                    if not os.path.exists(root + entry.name + '/posters/' + vdio.name[:-4] + '.jpg'):
                        jpg_task.write(root + entry.name + '\n')
                        jpg_task.write(vdio.name + '\n')

    gif_task.close()
    jpg_task.close()


def generate_task():  # generates multiple task files
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    filename_jpg_task = gv.getv('filename_jpg_task')
    filename_gif_task = gv.getv('filename_gif_task')
    number_of_programs_jpg = gv.getv('number_of_programs_jpg')
    number_of_programs_gif = gv.getv('number_of_programs_gif')
    filaname_jpg = root_main + 'task/' + filename_jpg_task
    filaname_gif = root_main + 'task/' + filename_gif_task
    filenames_jpg_arr = []
    filenames_gif_arr = []
    for i in range(number_of_programs_jpg):
        filenames_jpg_arr.append(filaname_jpg[:-4] + str(i) + '.txt')
    for i in range(number_of_programs_gif):
        filenames_gif_arr.append(filaname_gif[:-4] + str(i) + '.txt')
    files_jpg = [open(file, 'w') for file in filenames_jpg_arr]
    files_gif = [open(file, 'w') for file in filenames_gif_arr]

    count_jpg = 0
    count_gif = 0
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
            for vdio in os.scandir(root + entry.name + '/'):
                if vdio.is_file() and vdio.name[-4:] != '.ini':
                    if (not os.path.exists(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif')):
                        if number_of_programs_gif == 1:
                            files_gif[0].write(root + entry.name + '\n')
                            files_gif[0].write(vdio.name + '\n')
                        elif number_of_programs_gif > 1:
                            files_gif[count_gif].write(root + entry.name + '\n')
                            files_gif[count_gif].write(vdio.name + '\n')
                        count_gif = (count_gif + 1) % max(number_of_programs_gif, 1)
                    if (not os.path.exists(root + entry.name + '/posters/' + vdio.name[:-4] + '.jpg')):
                        if number_of_programs_jpg == 1:
                            files_jpg[count_jpg].write(root + entry.name + '\n')
                            files_jpg[count_jpg].write(vdio.name + '\n')
                        elif number_of_programs_jpg > 1:
                            files_jpg[count_jpg].write(root + entry.name + '\n')
                            files_jpg[count_jpg].write(vdio.name + '\n')
                        count_jpg = (count_jpg + 1) % max(number_of_programs_jpg, 1)
    for i in range(number_of_programs_jpg):
        files_jpg[i].close()
    for i in range(number_of_programs_gif):
        files_gif[i].close()

def open_window_generate_task():  # generates task in a single file
    text = ''
    layout = [[sg.Text(text, key='generate_task')], ]
    window = sg.Window("generate_task", layout)
    while True:
        event, values = window.read(timeout=0.001)
        if event == sg.WIN_CLOSED:
            break
        generate_task_old()
        window['generate_task'].update('Finished')
        window.refresh()

        break
    window.close()