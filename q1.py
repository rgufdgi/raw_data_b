#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 19:52:27 2024

@author: alex
"""
'''
тут в файлы данных, рассортированных по секциям, добавляется сумма амплитуд всех отчётов
'''
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
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


def qfun(value):
    summ = 0 
    lenn = int(len(value) / 4)
    #print(value)
    for i in range(lenn):
        num = u124(rverse(value[:4], 2), 2) 
        summ += num
        value = value[4:]
    return summ

start_time = datetime.now()  
print(start_time) 

for i in range(192, 216):
    name = f'/home/alex/baikal/files_13/new/sec_data{i}_13_1'
    
    data = pd.read_csv(name)
    values = data['values']
    q = []
    for j in range(len(values)):
        q.append(qfun(values[j]))
    #print(q)   
    data['q'] = q
    
    print(data['q'])
    data.to_csv(f'{name}', index=False)


end_time = datetime.now()  # время окончания выполнения
execution_time = end_time - start_time  # вычисляем время выполнения
 
print(f"Время выполнения программы: {execution_time}")





















