import json
import PySimpleGUI as sg

def str_to_arr(s):
    s.replace(' ', '')
    arr = int(s.split(','))
    return arr


def open_window_modify_json_main(flag_advanced):
    if flag_advanced:
        list_changeble = ['root_main', 'root_notepad', 'root_explorer', 'IP', 'port_start', 'arr_drives',
                        'drive_min_capacity', 'number_of_programs_jpg', 'number_of_programs_gif',
                        'number_of_video_per_random_page', 'db_host', 'db_user', 'db_password',
                        'db_database', 'number_of_video_per_entry_page']
    else:
        list_changeble = ['root_main', 'db_host', 'db_user', 'db_password', 'db_database']
    open_window_modify_json(list_changeble)

def open_window_modify_json(list_changeble):
    json_filename = './configs/config.json'
    with open(json_filename, "r") as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    layout = [[sg.Text('Modify the needed attributes')]]
    for key_name in list_changeble:
        layout.append([sg.Text(key_name, size=(15, 1)), sg.InputText(data[key_name], key = key_name)])
    layout.append([sg.Submit(), sg.Cancel()])
    window = sg.Window('Simple data entry window', layout)
    event, values = window.read()
    window.close()
    for key_name in list_changeble:
        if len(values[key_name]) > 0:
            data[key_name] = values[key_name]
    if len(values['arr_drives']) > 0:
        data['arr_drives'] = str_to_arr(values['arr_drives'])
    with open(json_filename, "w") as jsonFile:
        json.dump(data, jsonFile, indent = 2)
    jsonFile.close()

