#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:07:45 2024

@author: alex
"""
def datafile(i, data):
    with open(f'data_num{i}.txt', 'w') as file:
        for j in range(12):
            file.write(f'{data[208][11-j]}\t{data[193][11-j]}\t{data[211][11-j]}\n')
        for j in range(12):
            file.write(f'{data[207][11-j]}\t{data[192][11-j]}\t{data[210][11-j]}\n')
            
def color(num):
    if num < 50:
        return -1
    elif num < 1000:
        return 0
    elif num < 2000:
        return 1
    elif num < 4000:
        return 2
    elif num < 6000:
        return 3
    else: 
        return 4
    
def colorfile(f, i):
    with open(f, 'r') as file:
        colorfile = open(f'data_color{i}.txt', 'w')
        for _ in range(24):
            numbers = [int(c) for c in file.readline().split('\t')]
            colors = [color(n) for n in numbers]
            colorfile.write(f'{colors}\n')
        colorfile.close()

name = "noises13_q.txt"

l1 = {210:[], 211:[], 192:[], 193:[], 207:[], 208:[]}
l2 = {210:[], 211:[], 192:[], 193:[], 207:[], 208:[]}
l3 = {210:[], 211:[], 192:[], 193:[], 207:[], 208:[]}
l4 = {210:[], 211:[], 192:[], 193:[], 207:[], 208:[]}
l5 = {210:[], 211:[], 192:[], 193:[], 207:[], 208:[]}
l6 = {210:[], 211:[], 192:[], 193:[], 207:[], 208:[]}



count = 0
with open(name, 'r') as file:
    while True:
        zero = file.readline()
        sec = int(file.readline()[7:10])
        print(sec)
        if sec not in (210, 211, 192, 193, 207, 208):
            #continue
            break
        else:
            count += 1
            for i in range(12):
                data = file.readline().split('\t')[1:]
                for j in range(len(data)):
                   data[j] = data[j].split(' ')
                if i == 2:
                    print(data)
                signal1 = int(data[0][2])+int(data[0][4])+int(data[1][2])+int(data[1][4])
                signal2 = int(data[2][2])+int(data[2][4])+int(data[3][2])+int(data[3][4])
                signal3 = int(data[4][2])+int(data[4][4])+int(data[5][2])+int(data[5][4])
                signal4 = int(data[6][2])+int(data[6][4])+int(data[7][2])+int(data[7][4])
                signal5 = int(data[8][2])+int(data[8][4])+int(data[9][2])+int(data[9][4])
                signal6 = int(data[10][2])+int(data[10][4])+int(data[11][2])+int(data[11][4])
                    
                l1[sec].append(signal1)
                l2[sec].append(signal2)
                l3[sec].append(signal3)
                l4[sec].append(signal4)
                l5[sec].append(signal5)
                l6[sec].append(signal6)       
        if count == 6:
            print('done')
            break
        
#сохранение данных
datafile(1, l1)
datafile(2, l2)
datafile(3, l3)
datafile(4, l4)
datafile(5, l5)
datafile(6, l6)

#сортировка по цвету
colorfile("data_num1.txt", 1)
colorfile("data_num2.txt", 2)
colorfile("data_num3.txt", 3)
colorfile("data_num4.txt", 4)
colorfile("data_num5.txt", 5)
colorfile("data_num6.txt", 6)
            
    