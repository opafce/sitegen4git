import json
import PySimpleGUI as sg
from blocks import global_var as gv

def str_to_arr(s):
    print(s)
    arr = s.split(' ')
    arr_n = []
    for i in arr:
        arr_n.append(int(i))
    return arr_n
def arr_to_str(arr):
    s = ''
    for a in arr:
        s += str(a) + ' '
    return s[:-1]


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
    type_dict = {}
    for key_name in list_changeble:
        type_dict[key_name] = str(type(gv.getv(key_name))).replace("<class '", "").replace("'>", "")
    json_filename = './configs/config.json'
    with open(json_filename, "r") as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    layout = [[sg.Text('Modify the needed attributes')]]
    for key_name in list_changeble:
        if type_dict[key_name] == 'list':
            data[key_name] = arr_to_str(data['arr_drives'])
    for key_name in list_changeble:
        layout.append([sg.Text(key_name, size=(15, 1)), sg.InputText(data[key_name], key = key_name)])
    layout.append([sg.Button('submit'), sg.Button('cancel')])
    window = sg.Window('Simple data entry window', layout)
    event, values = window.read()
    window.close()
    if event == 'submit':
        for key_name in list_changeble:
            if len(values[key_name]) > 0:
                if type_dict[key_name] == 'str':
                    data[key_name] = values[key_name]
                elif type_dict[key_name] == 'int':
                    data[key_name] = int(values[key_name])
                elif type_dict[key_name] == 'list':
                    data[key_name] = str_to_arr(values[key_name])



        with open(json_filename, "w") as jsonFile:
            json.dump(data, jsonFile, indent = 2)
        jsonFile.close()

