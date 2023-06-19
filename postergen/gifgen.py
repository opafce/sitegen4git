from PIL import Image
import os
import cv2
import time
import shutil
import psutil
import socket
import sys
from blocks import global_var as gv



def create_gif(pathp, namep, size_of_task, gif_fps, fragments_sep_length, fragments_length, first_fragment_position, last_fragment_exclude_position, broken_videos):
    time_for_est = time.time()
    cam = cv2.VideoCapture(pathp + '/' + namep)
    # print(pathp+'/'+namep)
    try:
        if not os.path.exists(pathp + '/posters/gif'):
            os.makedirs(pathp + '/posters/gif')
    except OSError:
        print('Error: Creating directory of data')
    try:
        if not os.path.exists(pathp + '/posters/gif_raw'):
            os.makedirs(pathp + '/posters/gif_raw')
    except OSError:
        print('Error: Creating directory of data')
    percent = 0
    # if os.path.exists(pathp +'/posters/gif/' + namep[:-4] + '.gif'):
    # shutil.rmtree(pathp +'/posters/gif/' + namep[:-4] + '.gif', ignore_errors=True)
    if not os.path.exists(pathp + '/posters/gif/' + namep[:-4] + '.gif'):
        # print('Started...' + pathp + '/' + namep)
        frame_count = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cam.get(cv2.CAP_PROP_FPS)
        frame_arr = []
        video_length = int(frame_count / fps)
        multiplier = max(1.0, fps / gif_fps)
        len_gif = int((int((
                                       video_length * 2 / 3 - last_fragment_exclude_position - fragments_length * fps / 1000 / multiplier) / fragments_sep_length) + 1) * fragments_length / 1000)
        frame_number = frame_count // 3
        for j in range(round(fragments_length * fps / 1000 / multiplier)):
            frame_arr.append(round(frame_number + j * multiplier))

        for i in range(1, len_gif + 1):
            for j in range(round(fragments_length * fps / 1000 / multiplier)):
                frame_arr.append(round(frame_number + i * fragments_sep_length * fps + j * multiplier))

        len_gif2 = int((int((
                                        video_length / 3 - first_fragment_position - fragments_length * fps / 1000 / multiplier) / fragments_sep_length) + 1) * fragments_length / 1000)

        for j in range(round(fragments_length * fps / 1000 / multiplier)):
            frame_arr.append(round(first_fragment_position * fps + j * multiplier))

        for i in range(1, len_gif2):
            for j in range(round(fragments_length * fps / 1000 / multiplier)):
                frame_arr.append(round(i * fragments_sep_length * fps + j * multiplier))
        frames = []
        # for fr in frame_arr:
        # print(fr)
        MAX_SIZE = (640, 480)
        cnt_correct_image_shift = 0
        time_start_frame = time.time()
        time_per_frame = 1
        len_frame_arr = len(frame_arr)
        i = 0

        while True:
            cam = cv2.VideoCapture(pathp + '/' + namep)
            cam.set(cv2.CAP_PROP_POS_FRAMES, frame_arr[0] - 1 + cnt_correct_image_shift)
            res, frame = cam.read()
            str_output = str(PORT) + '***' + pathp + '/' + namep + '***' + str(
                int(i * 100 / len_frame_arr)) + '%' + '***' + str(
                int(time_per_frame * (100 - (i * 100 / len_frame_arr)))) + '***' + str(size_of_task)
            connection.send(str_output.encode('utf8'))
            if res:
                name = pathp + '/posters/gif_raw/' + namep[:-4] + '___' + str(frame_arr[0]) + '.jpg'
                cv2.imwrite(name, frame)
                frame1 = Image.open(name)
                frame1.thumbnail(MAX_SIZE)
                frame1.save(name)
                frame1 = Image.open(name)
                frames.append(frame1)
                break
            else:
                cnt_correct_image_shift += 1
                if cnt_correct_image_shift > 60:
                    f = open(broken_videos, 'a')
                    f.write(pathp + '/' + namep + '\n')
                    f.close()
                    break
            time_per_frame = time.time() - time_start_frame
            if time_per_frame > 3:
                cnt_correct_image_shift = 61

        for i in range(1, len_frame_arr):
            time_start_frame = time.time()
            while True:
                # print(int(100*i/len(frame_arr)), '%')
                # print(frame_arr[i]-1, cnt_correct_image_shift, frame_count)
                cam = cv2.VideoCapture(pathp + '/' + namep)
                cam.set(cv2.CAP_PROP_POS_FRAMES, frame_arr[i] - 1 + cnt_correct_image_shift)
                res, frame = cam.read()
                if res:
                    name = pathp + '/posters/gif_raw/' + namep[:-4] + '___' + str(
                        frame_arr[i] + cnt_correct_image_shift) + '.jpg'
                    cv2.imwrite(name, frame)
                    frame1 = Image.open(name)
                    frame1.thumbnail(MAX_SIZE)
                    frame1.save(name)
                    frame1 = Image.open(name)
                    frames.append(frame1)
                    break
                else:
                    cnt_correct_image_shift += 1
                    if cnt_correct_image_shift > 60:
                        f = open(broken_videos, 'a')
                        f.write(pathp + '/' + namep + '\n')
                        f.close()
                        break
            if cnt_correct_image_shift > 60:
                break
            time_per_frame = time.time() - time_start_frame
            if time_per_frame > 3:
                cnt_correct_image_shift = 61
            str_output = str(PORT) + '***' + pathp + '/' + namep + '***' + str(
                int(i * 100 / len_frame_arr)) + '%' + '***' + str(
                int(time_per_frame * (100 - (i * 100 / len_frame_arr)))) + '***' + str(size_of_task)
            connection.send(str_output.encode('utf8'))
            #print(str_output)
        str_output = str(PORT) + '***' + pathp + '/' + namep + ' -> saving'
        connection.send(str_output.encode('utf8'))
        frames[0].save(
            pathp + '/posters/gif/' + namep[:-4] + '.gif',
            quality=5,
            save_all=True,
            append_images=frames[1:],  # Срез который игнорирует первый кадр.
            optimize=True,
            duration=int(1 / min(fps, gif_fps) * 1000),
            loop=0)
        frame1.close()
        # print('Creating...' + name)
        shutil.rmtree(pathp + '/posters/gif_raw', ignore_errors=True)


def generate_gif_main(root, gif_fps, fragments_sep_length, fragments_length, first_fragment_position, last_fragment_exclude_position, broken_videos):
    pathp = ''
    namev = ''
    count = 0
    with open(root) as file:
        for line in file:
            if count == 0:
                pathp = line[:-1]
            elif count == 1:
                namev = line[:-1]
            else:
                break
            count += 1
    #print(pathp + namev)
    file.close()
    with open(root, 'r') as fin:
        data = fin.read().splitlines(True)
    fin.close()
    size_of_task = len(data) // 2
    with open(root, 'w') as fout:
        fout.writelines(data[2:])
    fout.close()
    create_gif(pathp, namev, size_of_task, gif_fps, fragments_sep_length, fragments_length, first_fragment_position, last_fragment_exclude_position, broken_videos)






if __name__ == '__main__':
    IP = gv.getv('IP')
    PORT = int(sys.argv[2])
    #print('\n' + str(PORT) + '\n')
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((IP, PORT))
    listener.listen(0)
    connection, address = listener.accept()

    number_of_program = int(sys.argv[1])
    gif_fps = gv.getv('gif_fps')
    fragments_sep_length = gv.getv('fragments_sep_length')
    fragments_length = gv.getv('fragments_length')
    first_fragment_position = gv.getv('first_fragment_position')
    last_fragment_exclude_position = gv.getv('last_fragment_exclude_position')
    root = gv.getv('root_main') + 'task/gif_task.txt'
    broken_videos = gv.getv('root_main') + 'broken_video.txt'
    root = root[:-4] + str(number_of_program) + '.txt'
    cpu_per_filename = gv.getv('cpu_per_filename')
    cpu_per_file = open(cpu_per_filename, "r")
    cpu_max_load = int(cpu_per_file.read(2))
    cpu_per_file.close()
    size = os.path.getsize(root)
    while size > 0:
        cpu_per_file = open(cpu_per_filename, "r")
        cpu_max_load = int(cpu_per_file.read(2))
        cpu_per_file.close()
        load_cpu = psutil.cpu_percent(4)
        if load_cpu > cpu_max_load:
            time_start_sleep = time.time()
            while (time.time() - time_start_sleep) < 2:
                str_output = str(PORT) + '***' + 'sleeping'
                connection.send(str_output.encode('utf8'))
                #print('sleeping ... zzz')
                time.sleep(0.25)
        else:
            generate_gif_main(root, gif_fps, fragments_sep_length, fragments_length, first_fragment_position, last_fragment_exclude_position, broken_videos)
            size = os.path.getsize(root)

    if size == 0:
        str_output = str(PORT) + '***' + 'break'
        connection.send(str_output.encode('utf8'))
        while True:
            data = connection.recv(1024).decode("utf8")
            if data == 'break':
                connection.close()
                break
