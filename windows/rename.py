import os
from blocks import global_var as gv
import PySimpleGUI as sg
def rename_string(
        str):  # rename a filename string so it may be used later as a key in many different circumstances (replaces every english letter and digit with itself and russian letters with their english transcript and some special cases for special charactrers)
    a = str[:-4]

    new = ''
    for i in range(len(a)):
        if (a[i] == 'a'):
            new += 'a'
        elif (a[i] == 'b'):
            new += 'b'
        elif (a[i] == 'c'):
            new += 'c'
        elif (a[i] == 'd'):
            new += 'd'
        elif (a[i] == 'e'):
            new += 'e'
        elif (a[i] == 'f'):
            new += 'f'
        elif (a[i] == 'g'):
            new += 'g'
        elif (a[i] == 'h'):
            new += 'h'
        elif (a[i] == 'i'):
            new += 'i'
        elif (a[i] == 'j'):
            new += 'j'
        elif (a[i] == 'k'):
            new += 'k'
        elif (a[i] == 'l'):
            new += 'l'
        elif (a[i] == 'm'):
            new += 'm'
        elif (a[i] == 'n'):
            new += 'n'
        elif (a[i] == 'o'):
            new += 'o'
        elif (a[i] == 'p'):
            new += 'p'
        elif (a[i] == 'q'):
            new += 'q'
        elif (a[i] == 'r'):
            new += 'r'
        elif (a[i] == 's'):
            new += 's'
        elif (a[i] == 't'):
            new += 't'
        elif (a[i] == 'u'):
            new += 'u'
        elif (a[i] == 'v'):
            new += 'v'
        elif (a[i] == 'w'):
            new += 'w'
        elif (a[i] == 'x'):
            new += 'x'
        elif (a[i] == 'y'):
            new += 'y'
        elif (a[i] == 'z'):
            new += 'z'


        elif (a[i] == 'A'):
            new += 'A'
        elif (a[i] == 'B'):
            new += 'B'
        elif (a[i] == 'C'):
            new += 'C'
        elif (a[i] == 'D'):
            new += 'D'
        elif (a[i] == 'E'):
            new += 'E'
        elif (a[i] == 'F'):
            new += 'F'
        elif (a[i] == 'G'):
            new += 'G'
        elif (a[i] == 'H'):
            new += 'H'
        elif (a[i] == 'I'):
            new += 'I'
        elif (a[i] == 'J'):
            new += 'J'
        elif (a[i] == 'K'):
            new += 'K'
        elif (a[i] == 'L'):
            new += 'L'
        elif (a[i] == 'M'):
            new += 'M'
        elif (a[i] == 'N'):
            new += 'N'
        elif (a[i] == 'O'):
            new += 'O'
        elif (a[i] == 'P'):
            new += 'P'
        elif (a[i] == 'Q'):
            new += 'Q'
        elif (a[i] == 'R'):
            new += 'R'
        elif (a[i] == 'S'):
            new += 'S'
        elif (a[i] == 'T'):
            new += 'T'
        elif (a[i] == 'U'):
            new += 'U'
        elif (a[i] == 'V'):
            new += 'V'
        elif (a[i] == 'W'):
            new += 'W'
        elif (a[i] == 'X'):
            new += 'X'
        elif (a[i] == 'Y'):
            new += 'Y'
        elif (a[i] == 'Z'):
            new += 'Z'

        elif (a[i] == 'а'):
            new += 'a'
        elif (a[i] == 'б'):
            new += 'b'
        elif (a[i] == 'в'):
            new += 'v'
        elif (a[i] == 'г'):
            new += 'g'
        elif (a[i] == 'д'):
            new += 'd'
        elif (a[i] == 'е'):
            new += 'e'
        elif (a[i] == 'ё'):
            new += 'o'
        elif (a[i] == 'ж'):
            new += 'zh'
        elif (a[i] == 'з'):
            new += 'z'
        elif (a[i] == 'и'):
            new += 'i'
        elif (a[i] == 'й'):
            new += 'y'
        elif (a[i] == 'к'):
            new += 'k'
        elif (a[i] == 'л'):
            new += 'l'
        elif (a[i] == 'м'):
            new += 'm'
        elif (a[i] == 'н'):
            new += 'n'
        elif (a[i] == 'о'):
            new += 'o'
        elif (a[i] == 'п'):
            new += 'p'
        elif (a[i] == 'р'):
            new += 'r'
        elif (a[i] == 'с'):
            new += 's'
        elif (a[i] == 'т'):
            new += 't'
        elif (a[i] == 'у'):
            new += 'u'
        elif (a[i] == 'ф'):
            new += 'f'
        elif (a[i] == 'х'):
            new += 'h'
        elif (a[i] == 'ц'):
            new += 'ts'
        elif (a[i] == 'ч'):
            new += 'ch'
        elif (a[i] == 'ш'):
            new += 'sh'
        elif (a[i] == 'щ'):
            new += 'sh'
        elif (a[i] == 'ы'):
            new += 'i'
        elif (a[i] == 'э'):
            new += 'e'
        elif (a[i] == 'ю'):
            new += 'u'
        elif (a[i] == 'я'):
            new += 'a'


        elif (a[i] == 'А'):
            new += 'A'
        elif (a[i] == 'Б'):
            new += 'B'
        elif (a[i] == 'В'):
            new += 'V'
        elif (a[i] == 'Г'):
            new += 'G'
        elif (a[i] == 'Д'):
            new += 'D'
        elif (a[i] == 'Е'):
            new += 'Ye'
        elif (a[i] == 'Ё'):
            new += 'Yo'
        elif (a[i] == 'Ж'):
            new += 'Zh'
        elif (a[i] == 'З'):
            new += 'Z'
        elif (a[i] == 'И'):
            new += 'I'
        elif (a[i] == 'Й'):
            new += 'Y'
        elif (a[i] == 'К'):
            new += 'K'
        elif (a[i] == 'Л'):
            new += 'L'
        elif (a[i] == 'М'):
            new += 'M'
        elif (a[i] == 'Н'):
            new += 'N'
        elif (a[i] == 'О'):
            new += 'O'
        elif (a[i] == 'П'):
            new += 'P'
        elif (a[i] == 'Р'):
            new += 'R'
        elif (a[i] == 'С'):
            new += 'S'
        elif (a[i] == 'Т'):
            new += 'T'
        elif (a[i] == 'У'):
            new += 'U'
        elif (a[i] == 'Ф'):
            new += 'F'
        elif (a[i] == 'Х'):
            new += 'H'
        elif (a[i] == 'Ц'):
            new += 'W'
        elif (a[i] == 'Ч'):
            new += 'Ch'
        elif (a[i] == 'Ш'):
            new += 'Sh'
        elif (a[i] == 'Щ'):
            new += 'Sh'
        elif (a[i] == 'Ы'):
            new += 'I'
        elif (a[i] == 'Э'):
            new += 'E'
        elif (a[i] == 'Ю'):
            new += 'Yu'
        elif (a[i] == 'Я'):
            new += 'Ya'


        elif (a[i] == '1'):
            new += '1'
        elif (a[i] == '2'):
            new += '2'
        elif (a[i] == '3'):
            new += '3'
        elif (a[i] == '4'):
            new += '4'
        elif (a[i] == '5'):
            new += '5'
        elif (a[i] == '6'):
            new += '6'
        elif (a[i] == '7'):
            new += '7'
        elif (a[i] == '8'):
            new += '8'
        elif (a[i] == '9'):
            new += '9'
        elif (a[i] == '0'):
            new += '0'


        elif (a[i] == ' '):
            new += '_'
        elif (a[i] == '-'):
            new += '_'
        elif (a[i] == '&'):
            new += '_'
        elif (a[i] == ','):
            new += '_'
        elif (a[i] == '.'):
            new += '_'
        elif (a[i] == '_'):
            new += '_'
        elif (a[i] == '7'):
            new += '7'
        elif (a[i] == '8'):
            new += '8'
        elif (a[i] == '9'):
            new += '9'
        elif (a[i] == '0'):
            new += '0'

        else:
            new += ''

    b = str[-4:]
    a = new + b
    a = a.replace('__________', '_')
    a = a.replace('_________', '_')
    a = a.replace('________', '_')
    a = a.replace('_______', '_')
    a = a.replace('______', '_')
    a = a.replace('_____', '_')
    a = a.replace('____', '_')
    a = a.replace('___', '_')
    a = a.replace('__', '_')
    return a

def rename():  # renames all the existing videos in all folders to match the desired shape
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):

            for vdio in os.scandir(root + entry.name + '/'):
                if vdio.is_file() and vdio.name[-4:] != '.ini':
                    if vdio.name != rename_string(vdio.name):
                        os.rename(root + entry.name + '/' + vdio.name,
                                  root + entry.name + '/' + rename_string(vdio.name))
            if os.path.exists(root + entry.name + '/posters/'):
                for vdio in os.scandir(root + entry.name + '/posters/'):
                    if vdio.is_file() and vdio.name[-4:] != '.ini':
                        if vdio.name != rename_string(vdio.name):
                            os.rename(root + entry.name + '/posters/' + vdio.name,
                                      root + entry.name + '/posters/' + rename_string(vdio.name))
            if os.path.exists(root + entry.name + '/posters/gif/'):
                for vdio in os.scandir(root + entry.name + '/posters/gif/'):
                    if vdio.is_file() and vdio.name[-4:] != '.ini':
                        if vdio.name != rename_string(vdio.name):
                            os.rename(root + entry.name + '/posters/gif/' + vdio.name,
                                      root + entry.name + '/posters/gif/' + rename_string(vdio.name))

def open_window_rename():  # runs rename script

    text = ''
    layout = [[sg.Text(text, key='rename')], ]
    window = sg.Window("Rename", layout)
    while True:
        event, values = window.read(timeout=0.001)
        if event == sg.WIN_CLOSED:
            break
        rename()
        window['rename'].update('Finished')
        window.refresh()

        break
    window.close()