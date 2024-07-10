#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:21:44 2024

@author: alex
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
 
#байты считываются в нужном порядке, но внутри типа данных они перевёрнуты 
#функция rverse переворачивает их обратно, в зависимости от длины значения в байтах
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
        for c in num2:
            if c == '1':
                num2_conv += '0'
            else:
                num2_conv += '1'
        return -int(num2_conv, 2)


def floatt(hexx, byte): # перевод для 32-битового float
    num2 = hex_to_binary(hexx, byte)
    
    while len(num2) != 32:
        num2 = f'0{num2}'
    sign = num2[0]
    power = num2[1:9]
    mant = num2[9:]
    power10 = int(power, 2) - 127
    result = 2**power10
    for i in range(len(mant)):
        result += (2**(power10 - 1 - i)) * int(mant[i])

    if sign == 1:
        return -result
    else:
        return result
#функция для перевода времени из заголовка записей. Выодит либо unix, либо обычный формат
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

def read_rc(rc, time):  #основная функция для чтения временнх кадров (gir 6 rf 0), возвращает словарь
    global counter2
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
    formatt = i124(rverse(rc[224:232], 4), 4)
    timer_time = time_t(rc[136:152])
    local_time = time_loc(rc[112:128])
    
    rc_data = rc[256:]
    one_data_dict = {'time':[], 'timet':[], 'timel':[], 'sdc':[], 'om': [], 'n_filt': [], 'step':[], 'values':[], 'event_n':[], 'mask':[]}
    
    flag = len(rc_data)
    while flag > 1:
        counter2 += 1
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
    if flag <= 1:
        return None
    

def read_rc_gist(rc, time):  # основная функция для чтения гистограмм
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

# !!!с этой функцией что-то не так, она выдаёт странные значения!!!
def time_loc(timel): # секунды и микросекунды с момента старта рана
    seconds = i124(rverse(timel[:8], 4), 4)
    microseconds = i124(rverse(timel[8:], 4), 4)
    return [seconds, microseconds]

def time_t(timet):  #возвращает время в часах
    hours = u124(timet[:2], 1)
    minutes = u124(timet[2:4], 1)
    sec = u124(timet[4:6], 1)
    tens_nanosec = u124(timet[6:8], 1)
    milsec = u124(rverse(timet[8:12], 2), 2)
    micsec = u124(rverse(timet[12:16], 2), 2)
    sec = sec + milsec/1000 + micsec/1000000 + tens_nanosec/100000000
    hours += minutes/60 + sec/3600
    return hours
'''   функция для построения врем. кадров, в другом виде используется в raw_06
def data_for_plot(value, step):
    x = [i for i in range(0,5000,5)]
    y = [0 for _ in range(1000)]
    
    lenn = int(len(value) / 4)
    for i in range(lenn):
        num = u124(rverse(value[:4], 2), 2) 
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
'''      
#штука, чтобы следить за длиткльность работы программы, обычно несколько минут
start_time = datetime.now()  
print(start_time) 
        
        
#имя файла          
name = 'i0136_05.043'
#заготовка списков для глобальной таблицы, в них считывается файл, по ним будет идти основной цикл
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
        if sep != 'fdfcfb7a':  # в обратном порядке, потому что так он считывается с файла
            break

# заготовка для мастерных записей (врем. кадры)
dataset = {'time':[], 'timet':[], 'timel':[], 'sdc':[], 'om': [], 'n_filt': [], 'step':[],  'values':[], 'event_n':[], 'mask':[]}
filt = [] # не знаю, насколько это нужно. 
gist_data = {'time':[], 'timel':[], 'timet':[], 'sdc':[], 'hist':[]}

#заготовки для остальных записей
gir0 = {'pConfVersionMinor':[], 'pConfVersionMajor':[], 'pMinorVersion':[], 'pMajorVersion':[], 'NClust':[]}
gir1 = {'ID':[], 'adress':[], 'stat':[], 'dinam':[]}
gir4 = {1:[], 2:[], 4:[]}
gir7rf1 = {'Master':[], 'OM CC':[], 'U+5':[], 'U+12':[], 'U-12':[], 'UH':[], 'Temp':[], 'ErrCnt':[]}
gir7rf2 = {'Master':[], 'OM CC':[], 'Pulces':[], 'Pulce':[]}
gir7rf3 = {'Commutator':[], 'ChannelState':[]}
gir7rf4 = {0:[]}
gir7rf5 = {'Sensor':[], 'temp_data':[], 'hum_data':[], 'press_data':[], 'accel_data':[], 'mag_data':[]}
gir3 = {'rf':[], 'rc':[]}


counter = 0 # количество мастерных записей без данных (нулевые )
counter2 = 0 # количество мастерных записей прошедших цикл в функции
for i in range(len(rc_l)): #основной цикл по всем записям
    """
    if gir_l[i] != 6 or rf_l[i] != 0 :  # для не мастерных данных
        formatt = None
    else:    
        formatt = i124(rverse(rc_l[i][224:232], 4), 4)  # проверка на фильтрованность маст. данных
    filt.append(formatt)
    """
    if gir_l[i] == 6 and rf_l[i] == 0: # заполнение словаря для фильтрованных маст. данных
        '''
        try:
            dataset_i = read_rc(rc_l[i], time_l[i])  # ошибка возникает для записей, содержащих только 
                                                     # заголовок, буду их пока выкидывать 
        except:
            counter += 1
            continue
        '''
        dataset_i = read_rc(rc_l[i], time_l[i])
        
        if dataset_i == None:
            counter += 1
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
        
    elif gir_l[i] == 6 and rf_l[i] == 1:

        gist_data_i = read_rc_gist(rc_l[i], time_l[i])
        
        gist_data['timet'].extend(gist_data_i['timet'])
        gist_data['timel'].extend(gist_data_i['timel'])
        gist_data['time'].extend(gist_data_i['time'])
        gist_data['sdc'].extend(gist_data_i['sdc'])
        gist_data['hist'].extend(gist_data_i['hist'])
        
    elif gir_l[i] == 0:
        pConfVersionMinor = u124(rverse(rc_l[i][:8], 4), 4)
        pConfVersionMajor = u124(rverse(rc_l[i][8:16], 4), 4)
        pMinorVersion = u124(rverse(rc_l[i][16:24], 4), 4)
        pMajorVersion  = u124(rverse(rc_l[i][24:32], 4), 4)
        NClust = i124(rverse(rc_l[i][32:36], 2), 2)
        
        gir0['pConfVersionMinor'].append(pConfVersionMinor)
        gir0['pConfVersionMajor'].append(pConfVersionMajor)
        gir0['pMinorVersion'].append(pMinorVersion)
        gir0['pMajorVersion'].append(pMajorVersion)
        gir0['NClust'].append(NClust)
        
    elif gir_l[i] == 1:
        ID  = i124(rverse(rc_l[i][:8], 4), 4) - 2130640384  # наверное
        n_elements = i124(rverse(rc_l[i][8:16], 4), 4)
        n_size = i124(rverse(rc_l[i][16:24], 4), 4)
        
        for i in range(n_elements):
            #адресная часть
            rc_l[i] = rc_l[i][24:]
            cluster = i124(rverse(rc_l[i][:4], 2), 2)
            string = i124(rverse(rc_l[i][4:8], 2), 2)
            section = i124(rverse(rc_l[i][8:12], 2), 2)
            rc_l[i] = rc_l[i][12:]
            #if ID != 16:  # версия 3.9.0(а)
             #   delimStatic = rverse(rc_l[i][:8], 4)
              #  rc_l[i][8:]
            delimStatic = rverse(rc_l[i][:8], 4)
            rc_l[i][8:]   
            #if len(rc_l[i]) < 2:
             #   print('что-то не так')
              #  continue
            
            gir1['ID'].append(ID)
            gir1['adress'].append([cluster, string, section])
            # стат. и динам. части в зависимости от ID
            if ID == 1:
                stat = rc_l[i][:24]
                delimDynamic = rverse(rc_l[i][24:32], 4)
                rc_l[i] = rc_l[i][32:]
                dinam = rc_l[i][:102]
            elif ID == 20:
                stat = rc_l[i][:10]
                delimDynamic = rverse(rc_l[i][10:18], 4)
                rc_l[i] = rc_l[i][18:]
                dinam = rc_l[i][:38]
            elif ID == 2:
                stat = rc_l[i][:16]
                delimDynamic = rverse(rc_l[i][16:24], 4)
                rc_l[i] = rc_l[i][24:]
                dinam = rc_l[i][:24]
            elif ID == 21:
                stat = rc_l[i][:12]
                delimDynamic = rverse(rc_l[i][12:20], 4)
                rc_l[i] = rc_l[i][20:]
                dinam = rc_l[i][:36]
            elif ID == 10:
                stat = rc_l[i][:24]
                delimDynamic = rverse(rc_l[i][24:32], 4)
                rc_l[i] = rc_l[i][32:]
                dinam = rc_l[i][:66]
            elif ID == 11:
                stat = rc_l[i][:8]
                delimDynamic = rverse(rc_l[i][8:16], 4)
                rc_l[i] = rc_l[i][16:]
                dinam = rc_l[i][:100]
                
            elif ID == 14:
                stat = rc_l[i][:264]
                delimDynamic = rverse(rc_l[i][264:272], 4)
                rc_l[i] = rc_l[i][272:]
                dinam = rc_l[i][:196]
                
            elif ID == 12:
                stat = rc_l[i][:8]
                delimDynamic = rverse(rc_l[i][8:16], 4)
                rc_l[i] = rc_l[i][16:]
                dinam = rc_l[i][:4]
                
            elif ID == 15:
                stat = rc_l[i][:12]
                delimDynamic = rverse(rc_l[i][12:20], 4)
                rc_l[i] = rc_l[i][20:]
                dinam = rc_l[i][:74]
                
            elif ID == 16:
                #adr = rc_l[i][:16]  # версия 3.9.0(а)
                #gir1['adress'][i].append(adr)
                #delimStatic = rverse(rc_l[i][16:24], 4)
                #rc_l[i][24:]
                stat = rc_l[i][:40]
                delimDynamic = rverse(rc_l[i][40:48], 4)
                rc_l[i] = rc_l[i][48:]
                dinam = rc_l[i][:40]
                
            elif ID == 30:
                stat = rc_l[i][:8]
                delimDynamic = rverse(rc_l[i][8:16], 4)
                rc_l[i] = rc_l[i][16:]
                dinam = rc_l[i][:4]
                
            elif ID == 31:
                stat = rc_l[i][:8]
                delimDynamic = rverse(rc_l[i][8:16], 4)
                rc_l[i] = rc_l[i][16:]
                dinam = rc_l[i][:4]
            
            gir1['stat'].append(stat)
            gir1['dinam'].append(dinam)
    elif gir_l[i] == 4:
        if rf_l[i] == 1:
            gir4[1].append(rc_l[i])
        elif rf_l[i] == 2:
            gir4[2].append(rc_l[i])
        elif rf_l[i] == 4:
            gir4[4].append(rc_l[i])
    elif gir_l[i] == 7:
        if rf_l[i] == 1:
            Master = u124(rc_l[i][:2], 1)
            OM_CC = u124(rc_l[i][2:4], 1)
            U5 = floatt(rverse(rc_l[i][4:12], 4), 4)
            U12 = floatt(rverse(rc_l[i][12:20], 4), 4)
            U_12 = floatt(rverse(rc_l[i][20:28], 4), 4)
            UH  = floatt(rverse(rc_l[i][28:36], 4), 4)
            Temp = floatt(rverse(rc_l[i][36:44], 4), 4)
            ErrCnt = i124(rverse(rc_l[i][44:52], 4), 4)
            gir7rf1['Master'].append(Master)
            gir7rf1['OM CC'].append(OM_CC)
            gir7rf1['U+5'].append(U5)
            gir7rf1['U+12'].append(U12)
            gir7rf1['U-12'].append(U_12)
            gir7rf1['UH'].append(UH)
            gir7rf1['Temp'].append(Temp)
            gir7rf1['ErrCnt'].append(ErrCnt)
        elif rf_l[i] == 2:
            Master = u124(rc_l[i][:2], 1)
            OM_CC = u124(rc_l[i][2:4], 1)
            Pulces = u124(rverse(rc_l[i][4:8], 2), 2)
            pulce = ''
            rc_l[i] = rc_l[i][8:]
            for _ in range(Pulces):
                pulce += str(rverse(rc_l[i][:8], 4)) + ' '
                rc_l[i] = rc_l[i][8:]
            gir7rf2['Master'].append(Master)
            gir7rf2['OM CC'].append(OM_CC) 
            gir7rf2['Pulces'].append(Pulces) 
            gir7rf2['Pulce'].append(pulce) 
        elif rf_l[i] == 3:
            gir7rf3 = {'Commutator':[], 'ChannelState':[]}
            Commutator = u124(rc_l[i][:2], 1)
            rc_l[i] = rc_l[i][2:]
            ChannelState = []
            for _ in range(8):
                ChannelState.append(floatt(rverse(rc_l[i][:8], 4), 4))
                rc_l[i] = rc_l[i][8:]
            gir7rf3['Commutator'].append(Commutator) 
            gir7rf3['ChannelState'].append(ChannelState)
        elif rf_l[i] == 4:
            gir7rf4[0].append(rc_l[i])
        elif rf_l[i] == 5:
#gir7rf5 = {'Sensor':[], 'temp_data':[], 'hum_data':[], 'press_data':[], 'accel_data':[], 'mag_data':[]} 
            Sensor = u124(rc_l[i][:2], 1)
            
            num = u124(rverse(rc_l[i][2:6], 2), 2)  
            rc_l[i] =rc_l[i][6:]
            temp_data = []
            for _ in range(num):
                temp_data.append(rc_l[i][:2])
                rc_l[i] = rc_l[i][2:]
                
            num = u124(rverse(rc_l[i][:4], 2), 2)  
            rc_l[i] = rc_l[i][4:]
            hum_data = []
            for _ in range(num):
                hum_data.append(rc_l[i][:2])
                rc_l[i] = rc_l[i][2:]
                
            num = u124(rverse(rc_l[i][:4], 2), 2)  
            rc_l[i] = rc_l[i][4:]
            press_data = []
            for _ in range(num):
                press_data.append(rc_l[i][:2])
                rc_l[i] = rc_l[i][2:]
            
            num = u124(rverse(rc_l[i][:4], 2), 2)  
            rc_l[i] = rc_l[i][4:]
            accel_data = []
            for _ in range(num):
                accel_data.append(rc_l[i][:2])
                rc_l[i] = rc_l[i][2:]
                
            num = u124(rverse(rc_l[i][:4], 2), 2)  
            rc_l[i] = rc_l[i][4:]
            mag_data = []
            for _ in range(num):
                mag_data.append(rc_l[i][:2])
                rc_l[i] = rc_l[i][2:]
            gir7rf5['Sensor'].append(Sensor)
            gir7rf5['temp_data'].append(temp_data)
            gir7rf5['hum_data'].append(hum_data)
            gir7rf5['press_data'].append(press_data)
            gir7rf5['accel_data'].append(accel_data)
            gir7rf5['mag_data'].append(mag_data)
    elif gir_l[i] == 3:
        gir3['rf'].append(rf_l[i])
        gir3['rc'].append(rc_l[i])

# большая таблица
data0 = pd.DataFrame({'gir':gir_l, 'rl': rl_l, 'rf': rf_l, 'time': time_l, 'rc':rc_l })  

# создание и запись в файлы мастерных данных
data60 = pd.DataFrame(dataset)
data60.to_csv(f'/home/alex/baikal/{name}_60')
data61 = pd.DataFrame(gist_data)
data61.to_csv(f'/home/alex/baikal/{name}_61')

# создание и запись в файлы всего остального
data1 = pd.DataFrame(gir1)
data4 = pd.DataFrame(gir4)
data71 = pd.DataFrame(gir7rf1)
data72 = pd.DataFrame(gir7rf2)
data73 = pd.DataFrame(gir7rf3)
data74 = pd.DataFrame(gir7rf4)
data75 = pd.DataFrame(gir7rf5)
data3 = pd.DataFrame(gir3)

data1.to_csv(f'/home/alex/baikal/{name}_gir1')
data4.to_csv(f'/home/alex/baikal/{name}_gir4')
data71.to_csv(f'/home/alex/baikal/{name}_71')
data72.to_csv(f'/home/alex/baikal/{name}_72')
data73.to_csv(f'/home/alex/baikal/{name}_73')
data74.to_csv(f'/home/alex/baikal/{name}_74')
data75.to_csv(f'/home/alex/baikal/{name}_75')
data3.to_csv(f'/home/alex/baikal/{name}_gir3')


filt2 = data0['rl'] >= 152 
filt3 = data0['rl'] < 152 
filt = data0['gir'] != 6
#filt3 = data0['filt'] != 3009
print(data0.loc[filt])
print(data0.loc[filt2, 'rl'])
print(data0.loc[filt3, 'rl'])
#print(data0.loc[filt3])
#print(data60.loc[filt, 'step'])
print(data60)
print()
print(counter)
print(counter2)
end_time = datetime.now()  # время окончания выполнения
execution_time = end_time - start_time  # вычисляем время выполнения
print(f"Время выполнения программы: {execution_time} ")