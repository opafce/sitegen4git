from blocks import global_var as gv
import os
import codecs
from blocks.utilities import liner, get_size
import PySimpleGUI as sg
def update_progress():  # a function to generate the progress html file
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    otstup = gv.getv('otstup')
    otstup_per = gv.getv('otstup_per')
    otstup_n_video = gv.getv('otstup_n_video')
    otstup_size = gv.getv('otstup_size')
    size_of_font = gv.getv('size_of_font')
    from configs.templates import style_string_color
    file_html = codecs.open(root_main + "index1.html", "w", encoding='utf-8')
    video_all_n = 0
    jpg_all_n = 0
    gif_all_n = 0
    links_arr = []
    file_html.write('''<html>\n<head>\n<title>HTML File</title>\n<meta charset=utf-8>\n</head>\n<body>''')
    file_html.write(style_string_color)

    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
            links_arr.append(entry.name)
            links_arr.sort()

    for name in links_arr:
        for i in range(1, number_of_disks + 1):
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                if name == entry.name:
                    file_html.write(
                        '''<a href="entries/''' + entry.name + '''.html" style="font-size: ''' + size_of_font + '''px; font-family:monospace">''' + entry.name + '''</a>''')
                    n_video = 0
                    n_jpg = 0
                    n_gifs = 0
                    for vdio in os.scandir(root + entry.name + '/'):
                        if vdio.is_file() and vdio.name[-4:] != '.ini':
                            n_video += 1
                            if not os.path.exists(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif'):
                                pass
                            else:
                                n_gifs += 1
                            if os.path.exists(root + entry.name + '/posters/' + vdio.name[:-4] + '.jpg'):
                                n_jpg += 1
                    # creates a spreadsheet-styled list of progress lines, linear structure is made by liner func
                    if n_video != 0:
                        if (n_jpg * 100 // n_video) == 100:
                            file_html.write('''<span class="purpleText">''' + liner(entry.name, otstup) + str(
                                (n_jpg * 100 // n_video)) + '% ' + '''</span>&nbsp;\n''')
                        else:
                            file_html.write('''<span class="redText">''' + liner(entry.name, otstup) + liner(
                                str((n_jpg * 100 // n_video)), otstup_per) + str(
                                (n_jpg * 100 // n_video)) + '% ' + '''</span>&nbsp;\n''')
                        if (n_gifs * 100 // n_video) == 100:
                            file_html.write('''<span class="greenText">''' + str(
                                (n_gifs * 100 // n_video)) + '% ' + '''</span>\n''')
                        else:
                            file_html.write(
                                '''<span class="redText">''' + liner(str((n_gifs * 100 // n_video)), otstup_per) + str(
                                    (n_gifs * 100 // n_video)) + '% ' + '''</span>\n''')
                        file_html.write('''<span class="blackText">''' + liner(str(n_video), otstup_n_video) + str(
                            n_video) + 'шт.' + '''</span>&nbsp;\n''')
                        size_of_entry = str(int(get_size(root + entry.name) / (1024 * 1024 * 1024)))
                        file_html.write('''<span class="blackText">''' + liner(size_of_entry,
                                                                               otstup_size) + size_of_entry + 'гб' + '''</span>&nbsp;''' + "<br/>\n\n")
                    else:
                        file_html.write('''<span class="redText">''' + '0 video' + '''</span>''' + "<br/>\n")
                    video_all_n += n_video
                    jpg_all_n += n_jpg
                    gif_all_n += n_gifs

    file_html.write('''<p style="font-size: 50px">всего видео:''' + str(video_all_n) + '''</p>''')
    file_html.write(
        '''<p style="font-size: 50px">осталось обработать:''' + str(video_all_n - jpg_all_n) + ''' фото</p>''')
    file_html.write(
        '''<p style="font-size: 50px">осталось обработать:''' + str(video_all_n - gif_all_n) + ''' гифок</p>''')
    file_html.write('''<a href="index.html" style="font-size: 50px">''' + 'назад' + '''</a>''' + "<br/>")
    file_html.write('''</body>\n</html>''')

    file_html.close()

def open_window_update_progress():  # runs update_progress script
    from windows.update_progress import update_progress
    text = ''
    layout = [[sg.Text(text, key='update_progress')], ]
    window = sg.Window("Update progress", layout)
    while True:
        event, values = window.read(timeout=0.001)
        if event == sg.WIN_CLOSED:
            break

        update_progress()
        window['update_progress'].update('Finished')
        window.refresh()

        break
    window.close()