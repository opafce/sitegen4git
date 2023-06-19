from blocks import global_var as gv
import os
import shutil
import PySimpleGUI as sg
def not_mp4_main():  # makes a txt file with not_mp4 files
    root_main = gv.getv('root_main')
    filename_not_mp4_files = gv.getv('filename_not_mp4_files')
    number_of_disks = len(gv.getv('arr_drives'))
    not_mp4_file = open(root_main + filename_not_mp4_files, "w")
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
            for vdio in os.scandir(root + entry.name):
                if vdio.is_file():
                    video_name_tmp = vdio.name[-4:]
                    if vdio.name[-4:] != '.mp4' or video_name_tmp.replace('crdown', '') != vdio.name[-4:]:
                        not_mp4_file.write(root + entry.name + '/' + vdio.name + '\n')
                        try:
                            if not os.path.exists(root_main + 'not_mp4/' + entry.name):
                                os.makedirs(root_main + 'not_mp4/' + entry.name)
                        except OSError:
                            print('Error: Creating directory of data - not_mp4')
                        shutil.move(root + entry.name + '/' + vdio.name,
                                    root_main + 'not_mp4/' + entry.name + '/' + vdio.name)
    not_mp4_file.close()

def open_window_not_mp4_files():  # window that runs not_mp4 script
    text = ''
    layout = [[sg.Text(text, key='not_mp4')], ]
    window = sg.Window("Not mp4", layout)
    while True:
        event, values = window.read(timeout=0.001)
        if event == sg.WIN_CLOSED:
            break
        not_mp4_main()
        window['not_mp4'].update('Finished')
        window.refresh()

        break
    window.close()