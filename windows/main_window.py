import os
import PySimpleGUI as sg
from blocks import global_var as gv
from blocks.utilities import get_preview_left_number, broken_and_raw_gif_remove, folder_check, copy_like_btb_img

from windows.balance import open_window_balancer
from windows.broken_files import open_window_broken_files
from windows.extra_files import open_window_extra_files, open_window_remove_extra_files, open_window_remove_extra_files_from_db
from windows.not_mp4 import open_window_not_mp4_files
from windows.similar_files import open_window_similar_files, open_window_similar_list_auto_check
from windows.delete_auto import open_window_delete_list_auto_check, delete_list_clear
from windows.rename import open_window_rename
from windows.generate_task import open_window_generate_task
from windows.update_progress import open_window_update_progress
from windows.fill_db import open_window_fill_db
from windows.postergen import open_window_postergen
from windows.sitegen import open_window_generate_site
from windows.check_ios import open_window_check_ios

root_main = gv.getv('root_main')
number_of_disks = len(gv.getv('arr_drives'))

db_preloaded = []
db_preloaded_delete = []
def open_window_main():  # main window to run all the above functions
    folder_check()
    copy_like_btb_img()
    root_main = gv.getv('root_main')
    root_notepad = gv.getv('root_notepad')
    filename_balancer = gv.getv('filename_balancer')
    filename_broken_files = gv.getv('filename_broken_files')
    filename_extra_files = gv.getv('filename_extra_files')
    filename_not_mp4_files = gv.getv('filename_not_mp4_files')
    filename_similar_list = gv.getv('filename_similar_list')
    filename_similar_list_folder = gv.getv('filename_similar_list_folder')
    filename_jpg_task = gv.getv('filename_jpg_task')
    filename_gif_task = gv.getv('filename_gif_task')
    jpg_left, gif_left = get_preview_left_number()
    layout = [[sg.Text("Technical")],
              [sg.Button("Balancer_gen"), sg.Button("Balancer", button_color=('black', 'yellow'))],
              [sg.Button("Broken_files_gen"), sg.Button("Broken_files", button_color=('black', 'yellow'))],
              [sg.Button("Extra_files_gen"), sg.Button("Extra_files", button_color=('black', 'yellow'))],
              [sg.Button("Not_mp4_files_gen"), sg.Button("Not_mp4_files", button_color=('black', 'yellow'))],
              [sg.Button("Similar_files_gen"), sg.Button("Similar_files", button_color=('black', 'yellow'))],
              [sg.Button("Similar_files_auto_open")],
              [sg.Button("Delete_files_auto_open"), sg.Button('Delete_list_clear')],
              [sg.Button("Generate_task"), sg.Button("Gif_task", button_color=('black', 'yellow')),
               sg.Button("Jpg_task", button_color=('black', 'yellow'))],
              [sg.Text("Take care - result is unrevertable")],
              [sg.Button("Remove_extra_files", button_color=('black', 'orange')),
               sg.Button("Fill_db", button_color=('black', 'orange')),
               sg.Button("Rename", button_color=('black', 'orange'))],
              [sg.Text("Generate site")],
              [sg.Text('photo left: ' + str(jpg_left) + ', gif left: ' + str(gif_left), key='preview_left_main')],
              [sg.Button("jpg_only"), sg.Button("gif_only"),
               sg.Button("jpg_then_gif", button_color=('black', 'yellow')),
               sg.Button("jpg_and_gif", button_color=('black', 'orange'))],
              [sg.Button("Generate_site")],
              [sg.Button("Update_progress")],
              [],
              [sg.Button("Check_iOS"), sg.Button("iOS_verify")]
              ]

    # Create the window
    window = sg.Window("Video_tool", layout, default_element_size=(12, 1), resizable=True, finalize=True)

    # Create an event loop
    while True:

        event, values = window.read(timeout=0.001)
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break
        if event == 'Balancer_gen':
            open_window_balancer()
        if event == 'Balancer':
            os.system(root_notepad + ' ' + root_main + filename_balancer)
        if event == 'Broken_files_gen':
            open_window_broken_files()
        if event == 'Broken_files':
            os.system(root_notepad + ' ' + root_main + filename_broken_files)
        if event == 'Extra_files_gen':
            open_window_extra_files()
        if event == 'Extra_files':
            os.system(root_notepad + ' ' + root_main + filename_extra_files)
        if event == 'Not_mp4_files_gen':
            open_window_not_mp4_files()
        if event == 'Not_mp4_files':
            os.system(root_notepad + ' ' + root_main + filename_not_mp4_files)
        if event == 'Similar_files_gen':
            open_window_similar_files()
        if event == 'Similar_files':
            folder_flag = 0
            breakflag = 0

            layout1 = [[sg.Text('See all similar files?')],
                       [sg.Button("Yes"), sg.Button("Specific")]]
            window1 = sg.Window("Similar list auto check", layout1)
            while True:
                event1, values1 = window1.read()
                if event1 == sg.WIN_CLOSED:
                    breakflag = 1
                    break
                elif event1 == "Yes":
                    break
                elif event1 == "Specific":
                    folder_flag = 1
                    break
            window1.close()
            if breakflag == 0:
                if folder_flag == 0:
                    os.system(root_notepad + ' ' + root_main + filename_similar_list)
                else:
                    os.system(root_notepad + ' ' + root_main + filename_similar_list_folder)
        if event == 'Similar_files_auto_open':
            open_window_similar_list_auto_check()
        if event == 'Delete_files_auto_open':
            open_window_delete_list_auto_check()
        if event == 'Delete_list_clear':
            delete_list_clear()

        # if event == 'No_metadata_gen':
        # open_window_no_metadata()
        # if event == 'No_metadata':
        # os.system(root_notepad + ' ' + root_main + filename_no_metadata)
        if event == 'Rename':
            open_window_rename()
        if event == 'Generate_task':
            open_window_generate_task()
        if event == 'Jpg_task':
            os.system(root_notepad + ' ' + root_main + filename_jpg_task)
        if event == 'Gif_task':
            os.system(root_notepad + ' ' + root_main + filename_gif_task)
        if event == 'Remove_extra_files':
            open_window_remove_extra_files()
            open_window_remove_extra_files_from_db()
        if event == 'Update_progress':
            open_window_update_progress()
        if event == 'Fill_db':
            open_window_fill_db()
        if event == 'jpg_and_gif':
            open_window_postergen(6, 6)
            jpg_left, gif_left = get_preview_left_number()
            window['preview_left_main'].update('photo left: ' + str(jpg_left) + ', gif left: ' + str(gif_left))
            window.refresh()
            broken_and_raw_gif_remove()
        if event == 'jpg_then_gif':
            open_window_postergen(6, 0)
            jpg_left, gif_left = get_preview_left_number()
            window['preview_left_main'].update('photo left: ' + str(jpg_left) + ', gif left: ' + str(gif_left))
            window.refresh()
            open_window_postergen(0, 6)
            jpg_left, gif_left = get_preview_left_number()
            window['preview_left_main'].update('photo left: ' + str(jpg_left) + ', gif left: ' + str(gif_left))
            window.refresh()
            broken_and_raw_gif_remove()
        if event == 'jpg_only':
            open_window_postergen(6, 0)
            jpg_left, gif_left = get_preview_left_number()
            window['preview_left_main'].update('photo left: ' + str(jpg_left) + ', gif left: ' + str(gif_left))
            window.refresh()
        if event == 'gif_only':
            open_window_postergen(0, 6)
            jpg_left, gif_left = get_preview_left_number()
            window['preview_left_main'].update('photo left: ' + str(jpg_left) + ', gif left: ' + str(gif_left))
            window.refresh()
            broken_and_raw_gif_remove()
        if event == 'Generate_site':
            open_window_generate_site()
        if event == 'Check_iOS':
            open_window_check_ios(0)
        if event == 'iOS_verify':
            open_window_check_ios(1)

    window.close()