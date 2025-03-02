#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 14:09:59 2024

@author: alex
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


def om(dataset): 
    datafile = open('noises13_q.txt', 'a')
    head = 'low, mn, m, hn, n\t'*12
    datafile.write('вспышка лазера\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\n') 
    datafile.write(f'Секция {dataset["sdc"][0]} \t{head}\n')
    
    # laser strart/stop time
    laser = ((4693900000, 4763700000), (4766400000, 4836350000), (4841900000, 4911940000), (4914520000, 4984530000), (4990200000, 5060150000), (5062900000, 5132720000), (5138350000, 5208300000), (5210980000, 5280900000), (5286500000, 5356800000), (5359200000, 5429100000),  (5438200000, 5508100000), (5510800000, 5580750000))
    for i in range(12):
        filt = dataset['om'] == i
        newset = dataset.loc[filt]
        #куски времени для нормировки шума на секунду
        time1 = min(newset['t']) #начало
        time2 = max(newset['t']) #конец
        time1 = (4500000000 - time1)/1000000
        time2 = (time2 - 5650000000)/1000000
        
        #отсечение для линейной аппроксимации фона
        filt_n1 = newset['t'] < 4500000000  # кусок в начале
        noise_set1 = newset.loc[filt_n1]
        t_noise1 = noise_set1['t']
        y_noise1 = noise_set1['q']
        param1 = np.polyfit(t_noise1, y_noise1, 0)  #средняя амплитуда шума 1
        param1 = param1[0]
        
        filt_n2 = newset['t'] > 5650000000 # кусок в конце
        noise_set2 = newset.loc[filt_n2]
        t_noise2 = noise_set2['t']
        y_noise2 = noise_set2['q']
        param2 = np.polyfit(t_noise2, y_noise2, 0)  #средняя амплитуда шума 2
        param2 = param2[0]
        
        param = (param1 + param2) / 2  # средний шум из двух кусков
        noise_min = min(min(y_noise1), min(y_noise2)) #нижний край дорожки
        HW = param - noise_min #полуширина подоржки
        noise_max = param + HW #верхний край дорожки
        
        #количество событий в шумовых дорожках в секунду
        filt1 = (noise_set1['q'] < noise_max)
        filt2 = (noise_set2['q'] < noise_max) 
        a = noise_set1.loc[filt1]
        b = noise_set2.loc[filt2] 
        

        noise_events = (len(a['q'])/time1 + len(b['y'])/time2) / 2 # количество шумовых сигналов в секунду
        # количество событий над шумовыми дорожками
        all_events = (len(noise_set1['q'])/time1 + len(noise_set2['q'])/time2) / 2
        hight_noise_events = all_events - noise_events
        '''
        if i == 4:  #для рисования примера
            param_list1 = [param for _ in range(len(t_noise1))]
            #param_list2 = [param for _ in range(len(t_noise2))]
            param_list3 = [noise_max for _ in range(len(t_noise1))]
            param_list4 = [noise_min for _ in range(len(t_noise1))]
            #param_list5 = [noise_max for _ in range(len(t_noise2))]
            #param_list6 = [noise_min for _ in range(len(t_noise2))]
            
            fig1 = plt.figure()
            fig1.set_figheight(10)
            fig1.set_figwidth(15)
            fig1.suptitle('aaa')
            ax1 = fig1.add_subplot(111)
            #ax1.set_title(f'{num}, {i}')
            ax1.set_xlabel('время, мкс')
            ax1.set_ylabel('сигнал АЦП')
            plt.scatter(t_noise1, y_noise1, color = 'black', s=2, marker='*')
            plt.plot(t_noise1, param_list1)
            plt.plot(t_noise1, param_list3)
            plt.plot(t_noise1, param_list4)
            #plt.scatter(t_noise2, y_noise2, color = 'black', s=2, marker='*')
            #plt.plot(t_noise2, param_list2)
            #plt.plot(t_noise2, param_list5)
            #plt.plot(t_noise2, param_list6)
            plt.show()
        '''
        info_low = []
        info_middle = []
        info_middle_n = []
        info_hight = []
        info_hight_n = []
        omstr = ''
        # начало доставания шумов
        for j in range(len(laser)):
            # нижние события
            filt_left = newset['t'] > laser[j][0]
            newset_left = newset[filt_left]
            filt_right = newset_left['t'] < laser[j][1]
            newset_right = newset_left.loc[filt_right]
            filt_low = newset_right['q'] < noise_min
            newset_low = newset_right.loc[filt_low]
            low = len(newset_low)
            #print(i, j, low)
            info_low.append(low)
           
            
            #события внутри
            time = (laser[j][1] - laser[j][0])/1000000
            filt_not_low = newset_right['q'] > noise_min
            newset_notlow = newset_right.loc[filt_not_low]
            filt_not_low2 = newset_notlow['q'] < noise_max
            newset_notlow = newset_notlow.loc[filt_not_low2]
            middle = len(newset_notlow)
            info_middle_n.append(middle)
            middle -= int(noise_events*time)
            info_middle.append(middle)
            
            #события сверху
            filt_hight = newset_right['q'] > noise_max
            newset_hight = newset_right.loc[filt_hight]
            hight = len(newset_hight)
            info_hight_n.append(hight)
            hight -= int(hight_noise_events*time)
            info_hight.append(hight)
            
            omstr0 = f'{low} {info_middle_n[-1]} {middle} {info_hight_n[-1]} {hight}\t'
            #omstr0 = f'{low}\t'
            omstr += omstr0
            

        
        datafile.write(f'OM{i}\t{omstr}\n')
    datafile.close()
        
start_time = datetime.now()  
print(start_time)         


for i in range(208, 209):
    try:
        section_data = pd.read_csv(f'/home/alex/baikal/files_13/new/sec_data{i}_13_1', index_col=0)  
    except:
        print('!')
        continue
    
    #section_data.drop(columns=['Unnamed: 0.1', 'Unnamed: 0'], inplace=True)
    column_names = section_data.keys().tolist()
    print(column_names)
    om(section_data)
    '''
    filt1 = (section_data['t'] > 5575000000)  
    exset = section_data.loc[filt1]
    filt2 = (exset['t'] < 5585000000)
    exset = exset.loc[filt2]
    filt3 = exset['om'] == 3
    exset = exset.loc[filt3]
    # поиск начала лазера
    fig1 = plt.figure()
    fig1.set_figheight(10)
    fig1.set_figwidth(45)
    fig1.suptitle('aaa')
    ax1 = fig1.add_subplot(111)
    #ax1.set_title(f'{num}, {i}')
    ax1.set_xlabel('время, мкс')
    ax1.set_ylabel('сигнал АЦП')
    plt.grid(which='major')
    plt.grid(which='minor', linestyle=':')
    plt.tight_layout()
    plt.scatter(exset['t'], exset['y'], color = 'black', s=2, marker='*')
    plt.xticks(np.arange(5575000000, max(exset['t']), 200000.0))
    fig1.savefig('grid2.png')

    #plt.show()
    '''
    
    
    
    
    
    
    
    
    
    
end_time = datetime.now()  # время окончания выполнения
execution_time = end_time - start_time  # вычисляем время выполнения
 
print(f"Время выполнения программы: {execution_time}")