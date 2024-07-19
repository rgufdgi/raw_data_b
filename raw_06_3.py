#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 15:29:37 2024

@author: alex
"""



import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

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

def om(dataset, num):
    for i in range(12):
        filt = dataset['om'] == i
        newset = dataset.loc[filt]
        fig1 = plt.figure()
        fig1.set_figheight(10)
        fig1.set_figwidth(15)
        fig1.suptitle(f'{num}, {i}')
        ax1 = fig1.add_subplot(111)
        #ax1.set_title(f'{num}, {i}')
        ax1.set_xlabel('время, мкс')
        ax1.set_ylabel('сигнал АЦП')
        plt.scatter(newset['t'], newset['y'], color = 'black', s=2, marker='*')
        #plt.show()
        fig1.savefig(f'{num}_{i}OM.png')
        
def section(dataset, num):
    fig1 = plt.figure()
    fig1.set_figheight(10)
    fig1.set_figwidth(15)
    fig1.suptitle(f'секция {num}')
    ax1 = fig1.add_subplot(111)
    #ax1.set_title(f'{num}, {i}')
    ax1.set_xlabel('время, мкс')
    ax1.set_ylabel('сигнал АЦП')
    plt.scatter(dataset['t'], dataset['y'], color = 'black', s=2, marker='*')
    #plt.show()
    fig1.savefig(f'{num}_section.png')


start_time = datetime.now()  
print(start_time) 

sec_data192 = pd.read_csv('sec_data192')   
sec_data193 = pd.read_csv('sec_data193')  
sec_data194 = pd.read_csv('sec_data194')  
sec_data195 = pd.read_csv('sec_data195')    
sec_data196 = pd.read_csv('sec_data196')  
sec_data197 = pd.read_csv('sec_data197')  
sec_data207 = pd.read_csv('sec_data207')  
sec_data208 = pd.read_csv('sec_data208') 
sec_data209 = pd.read_csv('sec_data209')  
sec_data210 = pd.read_csv('sec_data210')  
sec_data211 = pd.read_csv('sec_data211')  
sec_data212 = pd.read_csv('sec_data212')  
sec_data213 = pd.read_csv('sec_data213')  
sec_data214 = pd.read_csv('sec_data214')  
sec_data215 = pd.read_csv('sec_data215')  
sec_data216 = pd.read_csv('sec_data216')  
sec_data217 = pd.read_csv('sec_data217')  
sec_data218 = pd.read_csv('sec_data218') 


'''
om(sec_data207, 207)
om(sec_data208, 208)
om(sec_data209, 209)
om(sec_data210, 210)
om(sec_data211, 211)
om(sec_data212, 212)
om(sec_data216, 216)
om(sec_data217, 217)
om(sec_data218, 218)
'''
section(sec_data192, 192)
section(sec_data193, 193)
section(sec_data194, 194)
section(sec_data195, 195)
section(sec_data196, 196)
section(sec_data197, 197)
section(sec_data207, 207)
section(sec_data208, 208)
section(sec_data209, 209)
section(sec_data210, 210)
section(sec_data211, 211)
section(sec_data212, 212)
section(sec_data213, 213)
section(sec_data214, 214)
section(sec_data215, 215)
section(sec_data216, 216)
section(sec_data217, 217)
section(sec_data218, 218)


































end_time = datetime.now()  # время окончания выполнения
execution_time = end_time - start_time  # вычисляем время выполнения
 
print(f"Время выполнения программы: {execution_time}")