from PIL import Image, ImageDraw, ImageFont
from blocks import global_var as gv
import os
import cv2
import psutil
import shutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# a little function to paste in different ammount of spaces defined by otstup constants
# to have row-like structure of the progress html file
def liner(str, n):
    a = ''
    for i in range(n - len(str)):
        a += '&nbsp;'
    return a

def create_image_tmp(text):  # creates an image of an entry when no poster is provided
    root_main = gv.getv('root_main')
    font1 = ImageFont.truetype('arial.ttf', int(1500 / len(text)))
    img = Image.new(mode="RGB", size=(1008, 567), color='grey')
    draw = ImageDraw.Draw(img)
    textwidth = draw.textlength(text, font=font1)
    width, height = img.size
    x = width / 2 - textwidth / 2
    y = height / 2 - int(1500 / len(text) / 2)
    draw.text((x, y), text, font=font1, fill='black')
    img.save(root_main + 'posters_entries_tmp/' + text + ".jpg")


def get_size(start_path):  # of a folder
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp) and f[:-3] != 'raw':
                total_size += os.path.getsize(fp)

    return total_size


def get_n_video():  # get number of video in all the arrays
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    cnt = 0
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
            for vdio in os.scandir(root + entry.name + '/'):
                if vdio.is_file():
                    cnt += 1
    return cnt

def height2video_quality(height):  # returns the quality of the video by height
    return_str1 = ''
    if height == 4320:
        return '8K'
    elif height == 2160:
        return '4K'
    elif height == 1440:
        return '2K'
    elif height == 1080:
        return 'FHD'
    elif height == 720:
        return 'HD'
    elif height <= 480:
        return 'SD'
    else:
        if height > 4320:
            return '8K+'
        elif height > 2160:
            return '4K+'
        elif height > 1440:
            return '2K+'
        elif height > 1080:
            return 'FHD+'
        elif height > 720:
            return 'HD+'
        elif height > 480:
            return 'SD+'

        # if height > 4320:
        #    return '>8K'
        # elif height >= 3240:
        #    return '<8K'
        # elif height > 2160:
        #    return '>4K'
        # elif height >= 1800:
        #    return '<4K'
        # elif height > 1440:
        #    return '>2K'
        # elif height >= 1260:
        #    return '<2K'
        # elif height > 1080:
        #    return '>FHD'
        # elif height >= 900:
        #    return '<FHD'
        # elif height > 720:
        #    return '<HD'
        # elif height >= 600:
        #    return '<HD'
        # elif height > 480:
        #    return '>SD'

def seconds_to_time(seconds):  # converts seconds to a string on format 00:00 (m,s) or 00:00:00 (h, m, s)
    output_string = ''
    if seconds > 3600:
        output_string += '0' + str(int(seconds / 3600)) + ':'
    output_string += str(int((seconds % 3600) / 600)) + str(int((seconds % 600) / 60)) + ':'
    output_string += str(int((seconds % 60) / 10)) + str(int(seconds % 10))
    return output_string

def get_video_duration(filename):  # gets the duration in seconds of a specific video
    cam = cv2.VideoCapture(filename)
    frame_count = cam.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cam.get(cv2.CAP_PROP_FPS)
    if (frame_count == 0.0) or (fps == 0.0):
        return "warning"
    else:
        duration = int(frame_count / fps)
        return duration

def get_video_quality(filename):  # gets the quality of a specific video
    cam = cv2.VideoCapture(filename)
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    quality = height2video_quality(height)
    return (quality)

def get_preview_left_number():  # gets the number of jpg and gif posters left to generate
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    video_all_n = 0
    jpg_all_n = 0
    gif_all_n = 0
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
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
            video_all_n += n_video
            jpg_all_n += n_jpg
            gif_all_n += n_gifs
    return video_all_n - jpg_all_n, video_all_n - gif_all_n

def broken_and_raw_gif_remove():  # removes all the brokoen gifs from all folders and also removes the gif_raw folders
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
            for vdio in os.scandir(root + entry.name + '/'):
                if vdio.is_file():
                    if os.path.exists(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif'):
                        if (os.path.getsize(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif') == 0):
                            os.remove(root + entry.name + '/posters/gif/' + vdio.name[:-4] + '.gif')
                    if os.path.exists(root + entry.name + '/posters/gif_raw'):
                        shutil.rmtree(root + entry.name + '/posters/gif_raw', ignore_errors=True)


def get_number_of_frames_by_duration(duration):  # seconds
    return int((int((duration / 3 - 360) / 300) + int(2 * duration / 3 / 300)) * 24 * 0.8)

def draw_figure(canvas, figure):  # draws a figure
    tkcanvas = FigureCanvasTkAgg(figure, canvas)
    tkcanvas.draw()
    tkcanvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return tkcanvas

def folder_check():
    root_main = gv.getv('root_main')
    number_of_disks = len(gv.getv('arr_drives'))
    if not os.path.exists(root_main + 'entries'):
        os.makedirs(root_main + 'entries')
    if not os.path.exists(root_main + 'extra'):
        os.makedirs(root_main + 'extra')
    if not os.path.exists(root_main + 'not_mp4'):
        os.makedirs(root_main + 'not_mp4')
    if not os.path.exists(root_main + 'posters_entries'):
        os.makedirs(root_main + 'posters_entries')
    if not os.path.exists(root_main + 'random_pages'):
        os.makedirs(root_main + 'random_pages')
    if not os.path.exists(root_main + 'task'):
        os.makedirs(root_main + 'task')
    if not os.path.exists(root_main + 'posters_entries_tmp'):
        os.makedirs(root_main + 'posters_entries_tmp')
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
            if not os.path.exists(root_main + 'entries/' + entry.name):
                os.makedirs(root_main + 'entries/' + entry.name)
            if not os.path.exists(root + entry.name + '/posters/'):
                os.makedirs(root + entry.name + '/posters/')
            if not os.path.exists(root + entry.name + '/posters/gif'):
                os.makedirs(root + entry.name + '/posters/gif')

def check_pid_existence(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def kill_python_process_by_pid(pid):
    if check_pid_existence(pid):
        process = psutil.Process(pid)
        if process.name() == 'python.exe':
            try:
                os.system(f'taskkill /pid {pid}')
            except:
                pass
            print(pid, ':found')
        else:
            print(pid, ':not_found')
    else:
        print(pid, ':not_exist')


def kill_postergen_processes():
    filename = gv.getv('pids_to_del_filename')
    if os.path.exists(filename) and os.path.getsize(filename) != 0:
        with open(filename) as file:
            for line in file:
                kill_python_process_by_pid(int(line.rstrip()))
        file.close()
    file = open(filename, "w")
    file.close()

def copy_like_btb_img():
    dst = gv.getv('root_main')
    if not os.path.exists(dst + 'like.jpg'):
        shutil.copy('./configs/like.jpg', dst + 'like.jpg')
    if not os.path.exists(dst + 'unlike.jpg'):
        shutil.copy('./configs/unlike.jpg', dst + 'unlike.jpg')

