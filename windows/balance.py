from blocks import global_var as gv
import os
from blocks.utilities import get_size
import PySimpleGUI as sg
def balance_main():  # balances the entry folders among multiple drives, returns a txt file
    root_main = gv.getv('root_main')
    filename_balancer = gv.getv('filename_balancer')
    arr_drives = gv.getv('arr_drives')
    drive_min_capacity = gv.getv('drive_min_capacity')
    number_of_disks = len(gv.getv('arr_drives'))
    balancer_file = open(root_main + filename_balancer, "w")
    str_arr = []
    for i in range(1, number_of_disks + 1):
        root = root_main + str(i) + '/' + str(i) + '/'
        for entry in os.scandir(root):
            str_arr.append(
                entry.name + '***' + str(int(get_size(root + entry.name) / (1024 * 1024 * 1024))) + '***' + str(i))
    str_arr.sort()
    sum_size = 0
    for a in str_arr:
        b = a.split('***')
        sum_size += int(b[1])
    drive_capacity_step = sum_size / sum(arr_drives)
    # balancer_file.write('drive_capacity_step = ' + str(int(drive_capacity_step)) + ' gb\n')

    cnt = 0
    cnt_max = len(str_arr)
    for i in range(1, number_of_disks + 1):
        tmp_sum = 0
        next_folder_size = 0
        while (tmp_sum < (arr_drives[
                              i - 1] * drive_capacity_step - next_folder_size / 2) or i == number_of_disks) and cnt < cnt_max:
            if cnt + 1 < cnt_max:
                a = str_arr[cnt + 1].split('***')
            next_folder_size = int(a[1])
            b = str_arr[cnt].split('***')
            if int(b[2]) != i:
                balancer_file.write(str(b[0]) + ' ' + str(b[1]) + '     ' + str(b[2]) + '->' + str(i) + '\n')
            tmp_sum += int(b[1])
            cnt += 1
        balancer_file.write('\nTotal capacity of drive ' + str(i) + ': ' + str(tmp_sum) + '/' + str(
            int(drive_min_capacity * arr_drives[i - 1])) + ' gb -> ' + str(
            int(drive_capacity_step * arr_drives[i - 1])) + ' gb\n\n')
    balancer_file.write('Free space: ' + str(sum(arr_drives) * drive_min_capacity - sum_size) + ' gb')
    balancer_file.close()

def open_window_balancer():  # runs balancer script
    text = ''
    layout = [[sg.Text(text, key='balancer')], ]
    window = sg.Window("Balancer", layout)
    while True:
        event, values = window.read(timeout=0.001)
        if event == sg.WIN_CLOSED:
            break
        balance_main()
        window['balancer'].update('Finished')
        window.refresh()

        break
    window.close()