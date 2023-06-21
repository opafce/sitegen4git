from blocks import global_var as gv
import PySimpleGUI as sg
import pymysql
import os
from PIL import Image
import shutil
import random
import time
from windows.fill_db import open_window_fill_db
from windows.extra_files import open_window_remove_extra_files_from_db
from blocks.utilities import seconds_to_time, create_image_tmp, get_n_video
from blocks.preload import preload_db

arr_root = []  # initialization of global arrays needed for building random pages structureg for later random chose from them
arr_relative_root = []
arr_entry = []
arr_vdio = []


def get_arr_of_entry_sorted_by_datetime():  # returns an array sorted by datetime
    arr_entry = {}
    db_host = gv.getv('db_host')
    db_user = gv.getv('db_user')
    db_password = gv.getv('db_password')
    db_database = gv.getv('db_database')
    number_of_disks = len(gv.getv('arr_drives'))
    root_main = gv.getv('root_main')
    con = pymysql.connect(host=db_host,
                          user=db_user,
                          password=db_password,
                          database=db_database,
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
    with con:
        cur = con.cursor()
        for i in range(1, number_of_disks + 1):
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                arr = []
                query1 = '''SELECT id_video FROM categories WHERE id_entry = "''' + entry.name + '''" ORDER BY datetime DESC;'''
                cur.execute(query1)
                rows = cur.fetchall()
                len_arr = len(rows)
                for i in range(len_arr):
                    arr.append(rows[i]['id_video'])
                arr_entry[entry.name] = arr.copy()
    return arr_entry



def generate_initial_random_list():
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    arr_root = []
    arr_relative_root = []
    arr_entry = []
    arr_vdio = []
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
            for vdio in os.scandir(root + entry.name + '/'):
                if vdio.is_file():
                    arr_root.append(root)
                    arr_relative_root.append(str(i) + '/' + str(i) + '/')
                    arr_entry.append(entry.name)
                    arr_vdio.append(vdio.name)
    return arr_root, arr_relative_root, arr_entry, arr_vdio


# rename of random pages so they appear in alphabetic order (aaa2.html>aaa10.html -> aaa00002.html<aaa00010.html)
def change_name(i, number_of_random_pages):

    n_of_zeros = len(str(number_of_random_pages)) - len(str(i)) + 1
    a = ''
    for j in range(n_of_zeros):
        a += '0'
    a += str(i)
    return a

# part of random pages family, generates the header files' chunks defined by input values
def print_video_into_html_header(root, relative_root, entry, vdio):
    str_html_header = ''
    str_html_header += "<script>\n"
    str_html_header += "function play_" + vdio[:-4] + "() {\n"
    str_html_header += '''document.getElementById("''' + vdio[
                                                         :-4] + '''").src = " ../''' + relative_root + entry + "/posters/gif/" + vdio[
                                                                                                                                 :-4] + '''.gif"}\n'''
    str_html_header += "function pause_" + vdio[:-4] + "() {\n"
    str_html_header += '''document.getElementById("''' + vdio[
                                                         :-4] + '''").src = " ../''' + relative_root + entry + "/posters/" + vdio[
                                                                                                                             :-4] + '''.jpg"}\n'''
    str_html_header += "</script>\n"
    return str_html_header


# part of random pages family, generates the footer files' chunks defined by input values
def print_video_into_html_footer(root, relative_root, entry, vdio, db_preloaded):
    from blocks.is_ckeck import is_liked, get_duration_and_quality

    # footer
    # get image size
    str_html_footer = ''
    if os.path.exists(root + entry + '/posters/' + vdio[:-4] + '.jpg'):
        img = Image.open(root + entry + '/posters/' + vdio[:-4] + '.jpg')
        wid, hgt = img.size
        ratio_img = hgt / wid
    else:
        ratio_img = 9 / 16
    duration, quality = get_duration_and_quality(entry, vdio[:-4], db_preloaded)
    # video block generation
    str_html_footer += '''<div class="container" >    \n<a target="_blank" href="../entries/''' + entry + '''/''' + vdio[
                                                                                                                    :-4] + '''.html''' + '''"style="color: white">\n'''
    str_html_footer += '''<img onmouseover="''' + "play_" + vdio[:-4] + "()"
    str_html_footer += '''" onmouseout="''' + "pause_" + vdio[:-4] + "()"
    str_html_footer += '''" ontouchstart="''' + "play_" + vdio[:-4] + "()"
    str_html_footer += '''" ontouchend="''' + "pause_" + vdio[:-4] + "()"
    str_html_footer += '''" ontouchenter="''' + "play_" + vdio[:-4] + "()"
    str_html_footer += '''" src=" ../''' + relative_root + entry + "/posters/" + vdio[:-4]
    str_html_footer += '''.jpg" width="1008" height="''' + str(int(1008 * ratio_img)) + '''" id="'''
    str_html_footer += vdio[:-4] + '''">\n'''
    str_html_footer += '''    <div class="top-left">''' + quality + '''</div>\n'''
    str_html_footer += '''    <div class="top-right">''' + seconds_to_time(int(duration)) + '''</div>\n</div><br/>'''
    if is_liked(entry, vdio[:-4], db_preloaded):
        str_html_footer += '''<img src="../unlike.jpg''' + '''" width="110" height="44">\n'''
    else:
        str_html_footer += '''<img src="../like.jpg''' + '''" width="110" height="44">\n'''
    return str_html_footer


def random_list_gen(arr_root, arr_relative_root, arr_entry, arr_vdio, ):  # main random gen function
    number_of_video_per_random_page = gv.getv('number_of_video_per_random_page')
    arr_root_r = []
    arr_relative_root_r = []
    arr_entry_r = []
    arr_vdio_r = []
    costyl = 0  # nice name for a counter, defines the stop condition of a random page generation process
    #   (at he end there is not much to choose from)
    while len(arr_root_r) < number_of_video_per_random_page:
        rnd = random.randrange(len(arr_root))
        if arr_entry[rnd] in arr_entry_r and costyl < 100:
            pass
        else:
            arr_root_r.append(arr_root[rnd])
            arr_root.pop(rnd)
            arr_relative_root_r.append(arr_relative_root[rnd])
            arr_relative_root.pop(rnd)
            arr_entry_r.append(arr_entry[rnd])
            arr_entry.pop(rnd)
            arr_vdio_r.append(arr_vdio[rnd])
            arr_vdio.pop(rnd)
        costyl += 1
    return arr_root_r, arr_relative_root_r, arr_entry_r, arr_vdio_r

def open_window_generate_site():  # a windowed script that generates all the pages of the site
    from windows.update_progress import update_progress
    db_preloaded = preload_db()
    from configs.templates import style_list_string, cat_1_3, cat_2_3, cat_3_3
    from blocks.is_ckeck import is_liked, get_duration_and_quality
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    number_of_random_pages = get_n_video() // gv.getv('number_of_video_per_random_page')
    number_of_video_per_random_page = gv.getv('number_of_video_per_random_page')
    estimation_number = gv.getv('estimation_number')
    number_of_video_per_entry_page = gv.getv('number_of_video_per_entry_page')
    db_host = gv.getv('db_host')
    db_user = gv.getv('db_user')
    db_password = gv.getv('db_password')
    db_database = gv.getv('db_database')
    arr_entry_date = get_arr_of_entry_sorted_by_datetime()
    open_window_fill_db()
    open_window_remove_extra_files_from_db()
    time_last = time.time()
    time_last2 = time.time()
    text = 'Started'
    exit_flag = 0
    progressbar_generate_site = [
        [sg.ProgressBar(1000, orientation='h', size=(51, 10), key='progressbar_generate_site')]]
    progressbar_random = [[sg.ProgressBar(1000, orientation='h', size=(51, 10), key='progressbar_random')]]
    layout = [[sg.Text(text, key='entry_name')],
              [sg.Frame('Progress', layout=progressbar_generate_site), sg.Text('Time left: ', key='generate_site')],
              [sg.Text('Random_gen', key='random1')],
              [sg.Frame('Progress', layout=progressbar_random), sg.Text('Time left: ', key='random2')]]
    window = sg.Window("Generate site", layout)
    progress_bar_generate_site = window['progressbar_generate_site']
    progress_bar_random = window['progressbar_random']
    est_time_arr = []
    for i in range(estimation_number):
        est_time_arr.append(3599)
    while True:
        if exit_flag:
            break
        event, values = window.read(timeout=0.001)
        if event == sg.WIN_CLOSED:
            break
        number_of_video = 0
        for i in range(1, number_of_disks + 1):
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                for vdio in os.scandir(root + entry.name + '/'):
                    if vdio.is_file() and vdio.name[-4:] != '.ini':
                        number_of_video += 1
        cnt = 0
        file_front = open(root_main + "index.html", "w", encoding='utf-8')
        # Adding the input data to the HTML file
        video_all_n = 0
        jpg_all_n = 0
        gif_all_n = 0
        file_front.write('''<html>\n<head>\n<title>Main window</title>\n<meta charset=utf-8>\n''')
        file_front.write(style_list_string)
        file_front.write('''<script type="text/javascript">\n  var imageURLs = ["./random_pages/random''' + change_name(
            1, number_of_random_pages) + '''.html"''')
        for i in range(2, number_of_random_pages + 1):
            file_front.write(''', "./random_pages/random''' + change_name(i, number_of_random_pages) + '''.html"''')
        file_front.write('''];\n''')
        file_front.write(
            '''  function getImageTag() {\n    var img = '<a href=\"';\n    var randomIndex = Math.floor(Math.random() * imageURLs.length);\n    img += imageURLs[randomIndex];\n    img += '\" style="font-size: 50px">случайные видео</a><br/>';\n    return img;}\n</script>\n</head>\n<body>''')
        file_front.write(
            '''<a href="index1.html" style="color:orange;font-weight:bold;font-size: 100px">''' + 'страница обработки' + '''</a>''' + "<br/><br/><br/><br/>\n")
        file_front.write(
            '''<script type="text/javascript">\n  document.write(getImageTag());\n</script><br/><br/><br/><br/>\n''')
        links_arr = []
        for i in range(1, number_of_disks + 1):
            if exit_flag:
                break
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                if exit_flag:
                    break
                links_arr.append(entry.name)
                if not os.path.exists(root + 'posters_entries_tmp/' + entry.name + ".jpg"):
                    create_image_tmp(entry.name)
        links_arr.sort()

        for name in links_arr:
            n_video = 0
            for i in range(1, number_of_disks + 1):
                root = root_main + str(i) + '/' + str(i) + '/'
                for entry in os.scandir(root):
                    if entry.name == name:
                        for vdio in os.scandir(root + entry.name + '/'):
                            if vdio.is_file() and vdio.name[-4:] != '.ini':
                                n_video += 1
            file_front.write(
                '''<div class="container" >\n    <a href="entries/''' + name + '/' + 'page_g1' + '''.html''' + '''" style="color: white">\n''')
            if not os.path.exists(root_main + 'posters_entries/' + name + ".jpg"):
                file_front.write(
                    '''    <img src="posters_entries_tmp/''' + name + '''.jpg" width="1008" height="567"><br/>\n''')
            else:
                file_front.write(
                    '''    <img src="posters_entries/''' + name + '''.jpg" width="1008" height="567"><br/>\n''')
            file_front.write('''    <div class="top-right">''' + str(n_video) + ' шт.' + '''</div>\n</div><br/>''')
        file_front.write('''</body>\n</html>''')
        file_front.close()
        footer_header_blocks_arr = {}
        for i in range(1, number_of_disks + 1):
            if exit_flag:
                break
            root = root_main + str(i) + '/' + str(i) + '/'
            for entry in os.scandir(root):
                if exit_flag:
                    break
                footer_header_blocks_arr[entry.name] = {}
                n_video = 0
                n_jpg = 0
                n_gifs = 0
                for vdio in os.scandir(root + entry.name + '/'):
                    if vdio.is_file() and vdio.name[-4:] == '.mp4':
                        if event == sg.WIN_CLOSED:
                            exit_flag = 1
                            file_vdio_single.close()
                            break
                        if not os.path.exists(root_main + 'entries/' + entry.name):
                            os.makedirs(root_main + 'entries/' + entry.name)
                for vdio in os.scandir(root + entry.name + '/'):
                    if vdio.is_file() and vdio.name[-4:] == '.mp4':

                        # single video page gen
                        file_vdio_single = open(
                            root_main + 'entries/' + entry.name + '''/''' + vdio.name[:-4] + '''.html''', "w",
                            encoding="utf-8")
                        file_vdio_single.write(
                            '''<html>\n<head>\n<title>HTML File</title>\n<meta charset=utf-8>\n</head>\n<body>\n''')
                        file_vdio_single.write('''<p>''' + vdio.name[:-4] + '''</p><br/>\n''')
                        file_vdio_single.write('''<video src="../../''' + str(i) + '''/''' + str(
                            i) + '''/''' + entry.name + '''/''' + vdio.name + '''" controls width="1000" height="600" poster = " ../../''' + str(
                            i) + '''/''' + str(i) + '''/''' + entry.name + "/posters/" + vdio.name[
                                                                                         :-4] + '''.jpg"></video> <br/>\n''')

                        if is_liked(entry.name, vdio.name[:-4], db_preloaded):
                            file_vdio_single.write(
                                '''<img src="../../unlike.jpg''' + '''" width="110" height="44">\n''')
                        else:
                            file_vdio_single.write('''<img src="../../like.jpg''' + '''" width="110" height="44">\n''')
                        file_vdio_single.write('''<p><a href="./cat_''' + vdio.name[
                                                                          :-4] + '''.php''' + '''" style="font-size: 100px">categories <br/>\n''')
                        tmp_entry = entry.name
                        file_vdio_single.write(
                            '''<a href="../''' + entry.name + '/' + 'page_g1' + '''.html" style="font-size: 100px">''' + tmp_entry.replace(
                                '_', ' ') + '''</a>''' + "<br/>\n")
                        file_vdio_single.write('''<a href="../../''' + str(i) + '''/''' + str(
                            i) + '''/''' + entry.name + '''/''' + vdio.name + '''" download style="font-size: 100px" >Скачать</a>''' + "<br/>\n")
                        file_vdio_single.close()

                        # dict to store header and footer blocks
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]] = {}
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]]['header'] = ''
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]]['footer'] = ''
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]]['disk_n'] = i

                        time.time()
                        cnt += 1
                        window['entry_name'].update(entry.name)
                        for j in range(estimation_number - 1):
                            est_time_arr[j] = est_time_arr[j + 1]
                        est_time_arr[estimation_number - 1] = (number_of_video - cnt) * (-time_last + time.time())

                        window['generate_site'].update(
                            'Time left: ' + seconds_to_time(sum(est_time_arr) / estimation_number) + ' s')
                        progress_bar_generate_site.UpdateBar(str(cnt / number_of_video * 1000))
                        window.refresh()
                        time_last = time.time()
                        event, values = window.read(timeout=0.001)
                        if event == sg.WIN_CLOSED:
                            exit_flag = 1
                            break
                        # create folder
                        if not os.path.exists(root_main + 'entries/' + entry.name):
                            os.makedirs(root_main + 'entries/' + entry.name)

                        # create gifs page
                        n_video += 1
                        # header with scripts
                        if not os.path.exists(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif'):
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]]['header'] += "<script>\n"
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                                'header'] += "function play_" + vdio.name[:-4] + "() {\n"
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                                'header'] += '''document.getElementById("''' + vdio.name[
                                                                               :-4] + '''").src = " ../../''' + str(
                                i) + '''/''' + str(i) + '''/''' + entry.name + "/posters/" + vdio.name[
                                                                                             :-4] + '''.jpg"}\n'''
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                                'header'] += "function pause_" + vdio.name[:-4] + "() {\n"
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                                'header'] += '''document.getElementById("''' + vdio.name[
                                                                               :-4] + '''").src = " ../../''' + str(
                                i) + '''/''' + str(i) + '''/''' + entry.name + "/posters/" + vdio.name[
                                                                                             :-4] + '''.jpg"}\n'''
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]]['header'] += "</script>\n"
                        else:
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]]['header'] += "<script>\n"
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                                'header'] += "function play_" + vdio.name[:-4] + "() {\n"
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                                'header'] += '''document.getElementById("''' + vdio.name[
                                                                               :-4] + '''").src = " ../../''' + str(
                                i) + '''/''' + str(i) + '''/''' + entry.name + "/posters/gif/" + vdio.name[
                                                                                                 :-4] + '''.gif"}\n'''
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                                'header'] += "function pause_" + vdio.name[:-4] + "() {\n"
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                                'header'] += '''document.getElementById("''' + vdio.name[
                                                                               :-4] + '''").src = " ../../''' + str(
                                i) + '''/''' + str(i) + '''/''' + entry.name + "/posters/" + vdio.name[
                                                                                             :-4] + '''.jpg"}\n'''
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]]['header'] += "</script>\n"
                            n_gifs += 1
                        if os.path.exists(root + entry.name + '/posters/' + vdio.name[:-4] + '.jpg'):
                            n_jpg += 1

                        # footer
                        # get image size to make the video haeight adjustable
                        if os.path.exists(root + entry.name + '/posters/' + vdio.name[:-4] + '.jpg'):
                            img = Image.open(root + entry.name + '/posters/' + vdio.name[:-4] + '.jpg')
                            wid, hgt = img.size
                            ratio_img = hgt / wid
                        else:
                            ratio_img = 9 / 16
                        duration, quality = get_duration_and_quality(entry.name, vdio.name[:-4], db_preloaded)
                        duration = seconds_to_time(int(duration))
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]]['footer'] += '''<p>''' + vdio.name[
                                                                                                      :-4] + '''</p><br/>\n'''
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                            'footer'] += '''<div class="container" >\n    <a target="_blank" href="''' + vdio.name[
                                                                                                         :-4] + '''.html''' + '''" style="color: white">\n'''
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                            'footer'] += '''    <img onmouseover="''' + "play_" + vdio.name[:-4] + "()"
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                            'footer'] += '''" onmouseout="''' + "pause_" + vdio.name[:-4] + "()"
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                            'footer'] += '''" ontouchstart="''' + "play_" + vdio.name[:-4] + "()"
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                            'footer'] += '''" ontouchend="''' + "pause_" + vdio.name[:-4] + "()"
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                            'footer'] += '''" ontouchenter="''' + "play_" + vdio.name[:-4] + "()"
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]]['footer'] += '''" src=" ../../''' + str(
                            i) + '''/''' + str(i) + '''/''' + entry.name + "/posters/" + vdio.name[:-4]
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                            'footer'] += '''.jpg" width="1008" height="''' + str(int(1008 * ratio_img)) + '''" id="'''
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]]['footer'] += vdio.name[:-4] + '''">\n'''
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                            'footer'] += '''    <div class="top-left">''' + quality + '''</div>\n'''
                        footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                            'footer'] += '''    <div class="top-right">''' + duration + '''</div>\n</div><br/>'''

                        file_vdio_categories = open(
                            root_main + 'entries/' + entry.name + '''/cat_''' + vdio.name[:-4] + '''.php''', "w")
                        file_vdio_categories.write(cat_1_3)
                        file_vdio_categories.write('\n')
                        file_vdio_categories.write(
                            '''        <input type = "submit" name = "delete" value = "delete" style="font-size: 100px;height:150px; width:500px"/>\n''')

                        if is_liked(entry.name, vdio.name[:-4], db_preloaded):
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                                'footer'] += '''<img src="../../unlike.jpg''' + '''" width="110" height="44">\n'''
                        else:
                            footer_header_blocks_arr[entry.name][vdio.name[:-4]][
                                'footer'] += '''<img src="../../like.jpg''' + '''" width="110" height="44">\n'''
                            file_vdio_categories.write(
                                '''        <input type = "submit" name = "likes" value = "not like" style="font-size: 100px;height:150px; width:500px"/> <br/>\n''')

                        file_vdio_categories.write('''    </div>\n    <div class = "bata">\n''')

                        if is_liked(entry.name, vdio.name[:-4], db_preloaded):
                            file_vdio_categories.write(
                                '''        <input type = "submit" name = "likes" value = "like" style="font-size: 100px;height:150px; width:500px"/> <br/>\n''')

                        file_vdio_categories.write(cat_2_3)
                        file_vdio_categories.write('''<p><a href="./''' + vdio.name[
                                                                          :-4] + '''.html''' + '''" style="font-size: 100px">back</a></p><br/>\n''')

                        file_vdio_categories.write(
                            '''</body>\n</html>\n<?php\n$connection = mysqli_connect("''' + db_host + '''", "''' + db_user + '''", "''' + db_password + '''");\n$db = mysqli_select_db($connection,  "''' + db_database + '''"); \n''')
                        file_vdio_categories.write("$id_video = '" + vdio.name[:-4] + "';\n")
                        file_vdio_categories.write("$id_entry = '" + entry.name + "';\n")

                        file_vdio_categories.write(cat_3_3)
                if exit_flag:
                    break

                video_all_n += n_video
                jpg_all_n += n_jpg
                gif_all_n += n_gifs

                entry_number_of_pages = n_video // number_of_video_per_entry_page + 1
                filenames_vdeo_arr = []
                for j in range(entry_number_of_pages):
                    filenames_vdeo_arr.append(
                        root_main + 'entries/' + entry.name + '''/''' + 'page_g' + str(j + 1) + '''.html''')
                files_vdeo_arr = [open(file, 'w', encoding='utf-8') for file in filenames_vdeo_arr]
                for j in range(entry_number_of_pages):
                    files_vdeo_arr[j].write('''<!DOCTYPE html>\n<html>\n<head>\n''')
                    files_vdeo_arr[j].write(style_list_string)
                cnt_build_entry = 0
                for vdio in arr_entry_date[entry.name]:
                    files_vdeo_arr[cnt_build_entry // number_of_video_per_entry_page].write(
                        footer_header_blocks_arr[entry.name][vdio]['header'])
                    cnt_build_entry += 1
                for j in range(entry_number_of_pages):
                    files_vdeo_arr[j].write('''</head>\n<body>\n''')
                for j in range(entry_number_of_pages):
                    for k in range(entry_number_of_pages):
                        if k != j:
                            files_vdeo_arr[j].write(
                                '''<a class="fcc-btn" href="./''' + 'page_g' + str(k + 1) + '''.html">''' + str(
                                    k + 1) + '''</a>''' + "\n")
                        else:
                            files_vdeo_arr[j].write(
                                '''<a class="fcc-btn-inactive" >''' + str(k + 1) + '''</a>''' + "\n")
                        if k == 9 or k == 16 or k == 23 or k == 30:
                            files_vdeo_arr[j].write('''<br/><br/><br/>''')
                    files_vdeo_arr[j].write('''<br/><br/><br/>''')
                cnt_build_entry = 0
                for vdio in arr_entry_date[entry.name]:
                    files_vdeo_arr[cnt_build_entry // number_of_video_per_entry_page].write(
                        footer_header_blocks_arr[entry.name][vdio]['footer'])
                    cnt_build_entry += 1
                for j in range(entry_number_of_pages):
                    files_vdeo_arr[j].write(
                        '''<a href="../../index.html" style="font-size: 100px">back</a>''' + "<br/><br/>\n")
                for j in range(entry_number_of_pages):
                    for k in range(entry_number_of_pages):
                        if k != j:
                            files_vdeo_arr[j].write(
                                '''<a class="fcc-btn" href="./''' + 'page_g' + str(k + 1) + '''.html">''' + str(
                                    k + 1) + '''</a>''' + "\n")
                        else:
                            files_vdeo_arr[j].write(
                                '''<a class="fcc-btn-inactive" >''' + str(k + 1) + '''</a>''' + "\n")
                        if k == 9 or k == 16 or k == 23 or k == 30:
                            files_vdeo_arr[j].write('''<br/><br/><br/>''')

                for j in range(entry_number_of_pages):
                    files_vdeo_arr[j].write(
                        '''<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/></body>\n</html>''')
                    files_vdeo_arr[j].close()

            if exit_flag:
                break

        if exit_flag:
            break

        update_progress()
        # random part generate
        arr_root, arr_relative_root, arr_entry, arr_vdio = generate_initial_random_list()
        if exit_flag:
            break
        percent = 0
        cnt = 0
        if exit_flag:
            break
        else:
            shutil.rmtree(root_main + 'random_pages', ignore_errors=True)
            try:
                if not os.path.exists(root_main + 'random_pages'):
                    os.makedirs(root_main + 'random_pages')
            except OSError:
                print('Error: Creating directory of data - sitegen')

        for j in range(1, number_of_random_pages + 1):
            cnt += 1
            if exit_flag:
                break
            window['random2'].update(
                'Time left: ' + seconds_to_time((number_of_random_pages - cnt) * (-time_last2 + time.time())) + ' s')

            progress_bar_random.UpdateBar(str(cnt / number_of_random_pages * 1000))
            time_last2 = time.time()
            filename_r = root_main + 'random_pages/random' + change_name(j, number_of_random_pages) + '''.html'''
            file_random = open(filename_r, "w")
            file_random.write('''<html>\n<head>\n<title>Random</title>\n''')
            file_random.write(style_list_string)
            file_random.write(
                '''<script type="text/javascript">\n  var imageURLs = ["./random''' + change_name(1, number_of_random_pages) + '''.html"''')
            for i in range(2, number_of_random_pages + 1):
                file_random.write(''', "./random''' + change_name(i, number_of_random_pages) + '''.html"''')
            file_random.write('''];\n''')
            file_random.write(
                '''  function getImageTag() {\n    var img = '<p><a href=\"';\n    var randomIndex = Math.floor(Math.random() * imageURLs.length);\n    img += imageURLs[randomIndex];\n    img += '\" style="font-size: 100px; text-align:right;">ещё случайные видео</a></p><br/>';\n    return img;}\n</script>\n''')
            arr_root_r, arr_relative_root_r, arr_entry_r, arr_vdio_r = random_list_gen(arr_root, arr_relative_root, arr_entry, arr_vdio)
            for i in range(number_of_video_per_random_page):
                str_html_header = print_video_into_html_header(arr_root_r[i], arr_relative_root_r[i], arr_entry_r[i], arr_vdio_r[i])
                file_random.write(str_html_header)
            file_random.write('''</head>\n<body>\n''')
            file_random.write(
                '''<p><center><a href="../index.html" '''  '''style="font-size: 50px">назад</a></center></p><br/><br/><br/>\n''')
            for i in range(number_of_video_per_random_page):
                str_html_footer = print_video_into_html_footer(arr_root_r[i], arr_relative_root_r[i], arr_entry_r[i],
                                                               arr_vdio_r[i], db_preloaded)
                # file_random.write('''<p><center><a href="''' +'''../entries/''' + arr_entry_r[i] +'''.html" '''  '''style="font-size: 50px">''' + arr_entry_r[i] + '''</a></center></p><br/>\n''')
                file_random.write(str_html_footer)
            file_random.write('''<script type="text/javascript">\n  document.write(getImageTag());\n</script>\n''')
            event, values = window.read(timeout=0.001)
            if event == sg.WIN_CLOSED:
                exit_flag = 1
                file_random.close()
                break
            file_random.write(
                '''<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/></body>\n</html>''')
            if ((j - 1) * 100) / number_of_random_pages >= percent:
                percent += 1
        if exit_flag:
            break
        window['generate_site'].update('Finished')
        window.refresh()
        break
    window.close()