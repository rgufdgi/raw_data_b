#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:21:44 2024

@author: alex
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
 

def rverse(hexx, lenn):

    if len(hexx) == 4: #(lenn = 2)
        new_hex = hexx[2:]
        new_hex += hexx[:2]
        return new_hex
    if len(hexx) == 8: #lenn =4
        new_hex = hexx[6:]
        new_hex += hexx[4:6]
        new_hex += hexx[2:4]
        new_hex += hexx[:2]
        return new_hex
    else:
        lenn = lenn*2
        new_hex = hexx[lenn-2:]
        while lenn - 4 >= 0:
            new_hex += hexx[lenn-4 : lenn-2]
            lenn -= 2
        return new_hex
    
def hex_to_binary(num16, byte):  # перевод из 16ричной в двоичную
    num10 = int(num16, 16)
    num2 = bin(num10)[2:]
    if byte == 1:
        while len(num2) != 8:
            num2 = f'0{num2}'
    if byte == 2:
        while len(num2) != 16:
            num2 = f'0{num2}'
    if byte == 4:
        while len(num2) != 32:
            num2 = f'0{num2}'
    return num2


#ЛОЖЬ И НЕПРАВДА
# перевод из 16ричной в двоичную для разного количества байт
'''
def hex_to_b_mult(num1, num2, num3, num4): 
    if num1 == True:
        return hex_to_binary(f'{num1}{num2}{num3}{num4}')
    elif num2 == True:
        return hex_to_binary(f'{num2}{num3}{num4}')
    elif num3 == True:
        return hex_to_binary(f'{num3}{num4}')
    else:
        return hex_to_binary(num4)
'''   
    
def u124(num16, byte):  # перевод для беззнаковых типов данных
    num2 = hex_to_binary(num16, byte)
    return int(num2, 2)

def i124(num16, byte):  # перевод для знаковых типов данных
    num2 = hex_to_binary(num16, byte)

    if num2[0] == '0':  # положительные числа
        return int(num2, 2)
    else:  # отрицательные числа
        num2 = bin(int(num2, 2) - 1)[2:]

        num2_conv = ''
        #print('&')
        for c in num2:
            if c == '1':
                #print('!')
                num2_conv += '0'
            else:
                num2_conv += '1'
        return -int(num2_conv, 2)


def floatt(hexx):

    num2 = hex_to_binary(hexx)
    while len(num2) != 32:
        num2 = f'0{num2}'

    sign = num2[0]
    power = num2[1:9]
    mant = num2[9:]
    power10 = int(power, 2) - 127
    

    result = 2**power10
    print(result)
    for i in range(len(mant)):
        result += (2**(power10 - 1 - i)) * int(mant[i])

    
    #result = (2**power10) * int(mant, 2)
    if sign == 1:
        return -result
    else:
        return result

def time_func(time, if_unix):
    unix = u124(rverse(time[:8], 4), 4)
    year = u124(rverse(time[8:16], 4), 4)  
    month = u124(time[16:18], 1)
    day = u124(time[18:20], 1)
    hours = u124(time[20:22], 1)
    minutes = u124(time[22:24], 1)
    sec = u124(time[24:26], 1)
    milsec = u124(rverse(time[26:], 4), 4)
    
    sec += milsec/1000
    hours += minutes/60 + sec/3600 
    day += hours/24
    if if_unix == True:
        return unix
    else:
        return [year, month, day]

def read_rc(rc, time):
    '''
    head = rc[:255]
    sep = rc[:8]
    id1 = rc[8:16]
    #7fffff00
    record_type = rc[16:24]
    info_size_id = rc[24:32]
    info_size = i124(rverse(rc[32:40], 4), 4)
    event_size_id = rc[40:48]
    event_size = i124(rverse(rc[48:56], 4), 4)
    event_number_id = rc[56:64]
    event_number = rc[64:72]
    event_number_req_id = rc[72:80]
    event_number_req = rc[80:88]
    soft_event_number_id = rc[88:96]
    soft_event_number = rc[96:104]
    local_time_id = rc[104:112]
    local_time = rc[112:128]
    timer_time_id = rc[128:136]
    timer_time = rc[136:152]
    sdc_id = rc[152:160]
    sdc = rc[160:168]
    nplat_id = rc[168:176]
    nplat = rc[176:184]
    mask_id = rc[184:192]
    mask = rc[192:200]
    quality_id = rc[200:208]
    quality = rc[208:216]
    format_id = rc[216:224]
    formatt = i124(rverse(rc[224:232], 4), 4)
    tmask_id = rc[232:240]
    tmask = rc[240:248]
    data_id = rc[248:256] 
    '''
    #mask = hex_to_binary(rverse(rc[192:200], 4), 4) #тут нужно переводить не так
    mask = rverse(rc[192:200], 4)
    time = time_func(time, False)
    sdc = i124(rverse(rc[160:168], 4), 4)
    soft_event_number = i124(rverse(rc[96:104], 4), 4)
    #formatt = i124(rverse(rc[224:232], 4), 4)
    timer_time = time_t(rc[136:152])
    local_time = time_loc(rc[112:128])
    
    rc_data = rc[256:]
    one_data_dict = {'time':[], 'timet':[], 'timel':[], 'sdc':[], 'om': [], 'n_filt': [], 'step':[], 'values':[], 'event_n':[], 'mask':[]}
    
    while formatt == 3009:
        
        om = u124(rc_data[0:2], 1)
        nfilt = rc_data[2:4]
        
        n_bin = u124(rverse(rc_data[4:8], 2), 2)
        n_bin *= 2

        step = u124(rverse(rc_data[8:12], 2), 2)
        value = rc_data[16:n_bin*2 + 16]  
        
        one_data_dict['om'].append(om)
        one_data_dict['n_filt'].append(nfilt)
        one_data_dict['step'].append(step)
        one_data_dict['mask'].append(mask)
        one_data_dict['values'].append(value)
        one_data_dict['timet'].append(timer_time)
        one_data_dict['timel'].append(local_time)
        one_data_dict['time'].append(time)
        one_data_dict['event_n'].append(soft_event_number)
        #one_data_dict['filt'].append(True)
        one_data_dict['sdc'].append(sdc)
        
        rc_data = rc_data[n_bin*2 + 16:]
        if len(rc_data) < 2:
             break
        return one_data_dict
    

def read_rc_gist(rc, time):
    common_header_id = rc[:8]
    record_type_id = rc[8:16]
    record_type = rc[16:24]
    info_size_id = rc[24:32]
    info_size = rc[32:40]
    hist_size_id = rc[40:48]
    hist_size = rc[48:56]
    soft_hist_number_id = rc[56:64]
    soft_hist_number = rc[64:72]
    local_time_id = rc[72:80]
    local_time = rc[80:96]

    timer_time_id = rc[96:104]
    timer_time = rc[104:120]

    sdc_id = rc[120:128]
    sdc = rc[128:136]
    nplat_id = rc[136:144]
    nplat = rc[144:152]
    hist_mask_id= rc[152:160]
    hist_mask = rc[160:168]
    hist_format_id  = rc[168:176]
    hist_format = rc[176:184]
    hist_id= rc[184:192]
   
    time = time_func(time, False)
    timer_time = time_t(timer_time)
    local_time = time_loc(local_time)
    sdc = i124(rverse(sdc, 4), 4)
    soft_hist_number = i124(rverse(soft_hist_number, 4), 4)
    hist_format = i124(rverse(hist_format, 4), 4)
    
    data = rc[192:]
    
    gist_data = {'time':[], 'timel':[], 'timet':[], 'sdc':[],  'soft_hist_number':[], 'hist':[]}
    while len(data) > 0:
        gist = []
        if hist_format == 1024:
            for i in range(1024):
                val = u124(rverse(data[:4], 2), 2)
                gist.append(val)
                data = data[4:]
                gist_data['timet'].append(timer_time)
                gist_data['timel'].append(local_time)
                gist_data['time'].append(time)
                gist_data['sdc'].append(sdc)
                #gist_data['hist_format'].append(hist_format)
                gist_data['soft_hist_number'].append(soft_hist_number)
                gist_data['hist'].append(gist)
                
        else:
            for i in range(16):
                val = u124(rverse(data[:4], 2), 2)
                gist.append(val)
                data = data[4:]
                gist_data['timet'].append(timer_time)
                gist_data['timel'].append(local_time)
                gist_data['time'].append(time)
                gist_data['sdc'].append(sdc)
                #gist_data['hist_format'].append(hist_format)
                gist_data['soft_hist_number'].append(soft_hist_number)
                gist_data['hist'].append(gist)
        
    return gist_data

def time_loc(timel): # секунды и микросекунды с момента старта рана
    seconds = i124(rverse(timel[:8], 4), 4)
    microseconds = i124(rverse(timel[8:], 4), 4)
    return [seconds, microseconds]

def time_t(timet):
    hours = u124(timet[:2], 1)
    minutes = u124(timet[2:4], 1)
    sec = u124(timet[4:6], 1)
    tens_nanosec = u124(timet[6:8], 1)
    milsec = u124(rverse(timet[8:12], 2), 2)
    micsec = u124(rverse(timet[12:16], 2), 2)
    sec = sec + milsec/1000 + micsec/1000000 + tens_nanosec/100000000
    hours += minutes/60 + sec/3600
    return hours
    
def data_for_plot(value, step):
    x = [i for i in range(0,5000,5)]
    y = [0 for _ in range(1000)]
    
    lenn = int(len(value) / 4)
    for i in range(lenn):
        num = u124(rverse(value[:4], 2), 2) # нужен ли rverse?
        y[step + i] = num
        value = value[4:]
    fig1 = plt.figure(figsize=(12, 7))
    fig1.suptitle('что-то')
    ax1 = fig1.add_subplot(111)
    #ax1.set_title('EXO 040830-7134.7, exptime=20s')
    ax1.set_xlabel('Time, нс')
    ax1.set_ylabel('сигнал')
    #plt.scatter(x, y, color = 'black', s=10, marker='*')
    plt.plot(x,y)
    plt.show()
        
start_time = datetime.now()  
print(start_time) 
        
        
            
name = 'i0189_03.044'

gir_l = []
rl_l = []
rf_l = []
time_l = []
rc_l = []

with open(name, 'rb') as file: #открытие файла, считывание общей структуры
    while True:
        try:
            gir = rverse(file.read(2).hex(), 2)
            gir = i124(gir, 2)
            rl = rverse(file.read(4).hex(), 4)
            rl = i124(rl, 4)
            rf = rverse(file.read(2).hex(), 2)
            rf = i124(rf, 2)
            time = file.read(17).hex()
            rc = file.read(rl - 23).hex()
            sep = file.read(4).hex()
            if gir == 3 and rf == 100:
                sep = '1'
            
            gir_l.append(gir)
            rl_l.append(rl)
            rf_l.append(rf)
            time_l.append(time)
            rc_l.append(rc)
            
        except:
            print('Ошибка при чтении файла')
            sep = '1' 
        if sep != 'fdfcfb7a':
            break

# заготовка для мастерных записей (врем. кадры)
dataset = {'time':[], 'timet':[], 'timel':[], 'sdc':[], 'om': [], 'n_filt': [], 'step':[],  'values':[], 'event_n':[], 'mask':[]}
filt = []
gist_data = {'time':[], 'timel':[], 'timet':[], 'sdc':[], 'hist':[]}
gir0 = []
for i in range(len(rc_l)): #цикл по всем записям
    if gir_l[i] != 6 or rf_l[i] != 0 :  # для не мастерных данных
        formatt = None
    else:    
        formatt = i124(rverse(rc_l[i][224:232], 4), 4)  # проверка на фильтрованность маст. данных
    filt.append(formatt)
    
    if gir_l[i] == 6 and rf_l[i] == 0 and formatt == 3009: # заполнение словаря для фильтрованных маст. данных

        try:
            dataset_i = read_rc(rc_l[i], time_l[i])  # ошибка возникает для записей, содержащих только 
                                                     # заголовок, буду их пока выкидывать 
        except:
            continue
        
        if dataset_i == None:
            continue

        dataset['om'].extend(dataset_i['om'])
        dataset['n_filt'].extend(dataset_i['n_filt'])
        dataset['step'].extend(dataset_i['step'])
        dataset['values'].extend(dataset_i['values'])
        dataset['timet'].extend(dataset_i['timet'])
        dataset['timel'].extend(dataset_i['timel'])
        dataset['sdc'].extend(dataset_i['sdc'])
        dataset['time'].extend(dataset_i['time'])
        dataset['event_n'].extend(dataset_i['event_n'])
        dataset['mask'].extend(dataset_i['mask'])
        
    if gir_l[i] == 6 and rf_l[i] == 1:

        gist_data_i = read_rc_gist(rc_l[i], time_l[i])
        
        gist_data['timet'].extend(gist_data_i['timet'])
        gist_data['timel'].extend(gist_data_i['timel'])
        gist_data['time'].extend(gist_data_i['time'])
        gist_data['sdc'].extend(gist_data_i['sdc'])
        gist_data['hist'].extend(gist_data_i['hist'])
        
#    if gir_l[i] == 0:
        




data0 = pd.DataFrame({'gir':gir_l, 'rl': rl_l, 'rf': rf_l, 'time': time_l, 'rc':rc_l, 'filt':filt })  
data60 = pd.DataFrame(dataset)
data60.to_csv(f'/home/alex/baikal/{name}_60')
data61 = pd.DataFrame(gist_data)
data61.to_csv(f'/home/alex/baikal/{name}_61')




#filt = data60['step'] >= 1013
filt2 = data0['gir'] != 6

print(data0.loc[filt2])
#print(data60.loc[filt, 'step'])

end_time = datetime.now()  # время окончания выполнения
execution_time = end_time - start_time  # вычисляем время выполнения
 
print(f"Время выполнения программы: {execution_time} секунд")