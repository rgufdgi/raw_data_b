#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 19:00:47 2024

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
def hex_to_b_mult(num1, num2, num3, num4): 
    if num1 == True:
        return hex_to_binary(f'{num1}{num2}{num3}{num4}')
    elif num2 == True:
        return hex_to_binary(f'{num2}{num3}{num4}')
    elif num3 == True:
        return hex_to_binary(f'{num3}{num4}')
    else:
        return hex_to_binary(num4)
    
    
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


def timel(timel): # секунды и микросекунды с момента старта рана
    seconds = i124(rverse(timel[:8], 4), 4)
    microseconds = i124(rverse(timel[8:], 4), 4)
    return [seconds, microseconds]

def timer_time(timet):
    hours = u124(timet[:2], 1)
    minutes = u124(timet[2:4], 1)
    sec = u124(timet[4:6], 1)
    tens_nanosec = u124(timet[6:8], 1)
    milsec = u124(rverse(timet[8:12], 2), 2)
    micsec = u124(rverse(timet[12:16], 2), 2)
    
    return [hours, minutes, sec, milsec, micsec, tens_nanosec]

def data_for_plot(value, step):
    '''
    first_value = u124(rverse(value[:4], 2), 2)
    x = [i for i in range(0,5130,5)]
    y = [first_value - 100 for _ in range(1026)]
    '''
    x = [i for i in range(0,5130,5)]
    y = [0 for _ in range(1026)]
    
    
    lenn = int(len(value) / 4)
    try:
        for i in range(lenn):
            num = u124(rverse(value[:4], 2), 2) 
  
            y[step + i] = num
            value = value[4:]
            
        #return y[step-1:step+lenn +1], x[step-1:step+lenn +1]
        return y, x
    except IndexError:
       return 0, 0
start_time = datetime.now()  
print(start_time) 

name = 'i0189_03.044_60'

data = pd.read_csv(f'{name}')

print(data['values'])

print(data['step'])

values = list(data['values'])
step = list(data['step'])

counter = 0
impulse_x = []
impulse_y = []

# этот цикл сильно зависает 
for i in range(len(values)):


    a, b = data_for_plot(values[i], step[i])
    impulse_y.append(a)
    impulse_x.append(b)
    if i > 5000:
        print('done')
        break
#посмотреть другой способ, этот не работает
#data['impulse_y'], data['impulse_x'] = data['values'].apply(data_for_plot(data['values'], data['step'], False))
#data['impulse_y'], data['impulse_x'] = data_for_plot(data['values'], data['step'], False)



check = {'x': impulse_x, 'y': impulse_y}
df = pd.DataFrame(check)
print(df['x'])
filt = df['x'] == 0
print(df[filt])

print(len(impulse_y))

for i in range(5):
    x = impulse_x[100+i]
    y = impulse_y[100+i]
    fig1 = plt.figure(figsize=(12, 7))
    fig1.suptitle('временной кадр')
    ax1 = fig1.add_subplot(111)
    #ax1.set_title('EXO 040830-7134.7, exptime=20s')
    ax1.set_xlabel('Time, нс')
    ax1.set_ylabel('сигнал')
    #plt.scatter(x, y, color = 'black', s=10, marker='*')
    plt.plot(x,y)
    plt.show()



































































end_time = datetime.now()  # время окончания выполнения
execution_time = end_time - start_time  # вычисляем время выполнения
 
print(f"Время выполнения программы: {execution_time} секунд")