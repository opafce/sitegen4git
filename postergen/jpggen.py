import cv2
import time
from PIL import Image
import psutil
import socket
import os
import sys
from blocks import global_var as gv



def create_jpg(pathp, namep, size_of_task):
    try:
        if not os.path.exists(pathp + '/posters'):
            os.makedirs(pathp + '/posters')
    except OSError:
        print('Error: Creating directory of data')
    if not os.path.exists(pathp + '/posters/' + namep[:-4] + '.jpg'):
        cam = cv2.VideoCapture(pathp + '/' + namep)
        frame_number = int(cam.get(cv2.CAP_PROP_FRAME_COUNT)) // 3
        cam.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
        res, frame = cam.read()
        name = pathp + '/posters/' + namep[:-4] + '.jpg'
        cv2.imwrite(name, frame)
        frame1 = Image.open(name)
        MAX_SIZE = (1280, 720)
        frame1.thumbnail(MAX_SIZE)
        frame1.save(name)
        frame1.close()
        str_output = str(PORT) + '***' + pathp + '/' + namep + '***' + str(int(size_of_task / 2))
        connection.send(str_output.encode('utf8'))


def generate_jpg_main(root):
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
    size_of_task = len(data)
    with open(root, 'w') as fout:
        fout.writelines(data[2:])
    fout.close()
    create_jpg(pathp, namev, size_of_task)

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
    root = gv.getv('root_main') + 'task/jpg_task.txt'
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
                str_output = str(PORT) + '/' + '***' + 'sleeping'
                connection.send(str_output.encode('utf8'))
                #print('sleeping ... zzz')
                time.sleep(0.25)
        else:
            generate_jpg_main(root)
            size = os.path.getsize(root)
    if size == 0:
        str_output = str(PORT) + '***' + 'break'
        connection.send(str_output.encode('utf8'))
        while True:
            data = connection.recv(1024).decode("utf8")
            if data == 'break':
                connection.close()
                break






