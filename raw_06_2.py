#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 15:33:09 2024

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
   
def get_hhw(value, step):
    x = step + int(len(value)/4)
    lenn = int(len(value) / 4)
    for i in range(lenn):
        num = u124(rverse(value[:4], 2), 2) 
        if i == int(lenn/2):
            y = num
            break
        value = value[4:]
    return x, y



start_time = datetime.now()  
print(start_time) 

name = '/home/alex/baikal/files_13/new/n0075_13.0009_master2'


sec_data192 = pd.DataFrame()
sec_data193 = pd.DataFrame()
sec_data194 = pd.DataFrame()
sec_data195 = pd.DataFrame()
sec_data196 = pd.DataFrame()
sec_data197 = pd.DataFrame()
sec_data198 = pd.DataFrame()
sec_data199 = pd.DataFrame()
sec_data200 = pd.DataFrame()
sec_data201 = pd.DataFrame()
sec_data202 = pd.DataFrame()
sec_data203 = pd.DataFrame()
sec_data204 = pd.DataFrame()
sec_data205 = pd.DataFrame()
sec_data206 = pd.DataFrame()
sec_data207 = pd.DataFrame()
sec_data208 = pd.DataFrame()
sec_data209 = pd.DataFrame()
sec_data210 = pd.DataFrame()
sec_data211 = pd.DataFrame()
sec_data212 = pd.DataFrame()
sec_data213 = pd.DataFrame()
sec_data214 = pd.DataFrame()
sec_data215 = pd.DataFrame()
sec_data216 = pd.DataFrame()
sec_data217 = pd.DataFrame()
sec_data218 = pd.DataFrame()
'''
sec_data192 = pd.read_csv('sec_data192')
sec_data193 = pd.read_csv('sec_data193')
sec_data194 = pd.read_csv('sec_data194')
sec_data195 = pd.read_csv('sec_data195')
sec_data196 = pd.read_csv('sec_data196')
sec_data197 = pd.read_csv('sec_data197')
sec_data198 = pd.read_csv('sec_data198')
sec_data199 = pd.read_csv('sec_data199')
sec_data200 = pd.read_csv('sec_data200')
sec_data201 = pd.read_csv('sec_data201')
sec_data202 = pd.read_csv('sec_data202')
sec_data203 = pd.read_csv('sec_data203')
sec_data204 = pd.read_csv('sec_data204')
sec_data205 = pd.read_csv('sec_data205')
sec_data206 = pd.read_csv('sec_data206')
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

for i in range(9, 14):
    
    data = pd.read_csv(f'{name[:41]}00{i}_master2', index_col=0)
    '''
    if i < 10:
        data = pd.read_csv(f'{name[:42]}00{i}_60')
    else:
        data = pd.read_csv(f'{name[:42]}0{i}_60')
    '''    



# разделение по секциям
    filt1 = data['sdc'] == 192
    filt2 = data['sdc'] == 193
    filt3 = data['sdc'] == 194
    filt4 = data['sdc'] == 195
    filt5 = data['sdc'] == 196
    filt6 = data['sdc'] == 197
    filt7 = data['sdc'] == 198
    filt8 = data['sdc'] == 199
    filt9 = data['sdc'] == 200
    filt10 = data['sdc'] == 201
    filt11 = data['sdc'] == 202
    filt12 = data['sdc'] == 203
    filt13 = data['sdc'] == 204
    filt14 = data['sdc'] == 205
    filt15 = data['sdc'] == 206
    filt16 = data['sdc'] == 207
    filt17 = data['sdc'] == 208
    filt18 = data['sdc'] == 209
    filt19 = data['sdc'] == 210
    filt20 = data['sdc'] == 211
    filt21 = data['sdc'] == 212
    filt22 = data['sdc'] == 213
    filt23 = data['sdc'] == 214
    filt24 = data['sdc'] == 215
    #filt25 = data['sdc'] == 216
    #filt26 = data['sdc'] == 217
   # filt27 = data['sdc'] == 218
    
    data11 = data.loc[filt1]
    data12 = data.loc[filt2]
    data13 = data.loc[filt3]
    data21 = data.loc[filt4]
    data22 = data.loc[filt5]
    data23 = data.loc[filt6]
    data31 = data.loc[filt7]
    data32 = data.loc[filt8]
    data33 = data.loc[filt9]
    data41 = data.loc[filt10]
    data42 = data.loc[filt11]
    data43 = data.loc[filt12]
    data51 = data.loc[filt13]
    data52 = data.loc[filt14]
    data53 = data.loc[filt15]
    data61 = data.loc[filt16]
    data62 = data.loc[filt17]
    data63 = data.loc[filt18]
    data71 = data.loc[filt19]
    data72 = data.loc[filt20]
    data73 = data.loc[filt21]
    data81 = data.loc[filt22]
    data82 = data.loc[filt23]
    data83 = data.loc[filt24]
    #data91 = data.loc[filt25]
    #data92 = data.loc[filt26]
   # data93 = data.loc[filt27]
    
    
    sec_data192 = pd.concat([sec_data192, data11], ignore_index=True)
    sec_data193 = pd.concat([sec_data193, data12], ignore_index=True)
    sec_data194 = pd.concat([sec_data194, data13], ignore_index=True)
    sec_data195 = pd.concat([sec_data195, data21], ignore_index=True)
    sec_data196 = pd.concat([sec_data196, data22], ignore_index=True)
    sec_data197 = pd.concat([sec_data197, data23], ignore_index=True)
    sec_data198 = pd.concat([sec_data198, data31], ignore_index=True)
    sec_data199 = pd.concat([sec_data199, data32], ignore_index=True)
    sec_data200 = pd.concat([sec_data200, data33], ignore_index=True)
    sec_data201 = pd.concat([sec_data201, data41], ignore_index=True)
    sec_data202 = pd.concat([sec_data202, data42], ignore_index=True)
    sec_data203 = pd.concat([sec_data203, data43], ignore_index=True)
    sec_data204 = pd.concat([sec_data204, data51], ignore_index=True)
    sec_data205 = pd.concat([sec_data205, data52], ignore_index=True)
    sec_data206 = pd.concat([sec_data206, data53], ignore_index=True)
    sec_data207 = pd.concat([sec_data207, data61], ignore_index=True)
    sec_data208 = pd.concat([sec_data208, data62], ignore_index=True)
    sec_data209 = pd.concat([sec_data209, data63], ignore_index=True)
    sec_data210 = pd.concat([sec_data210, data71], ignore_index=True)
    sec_data211 = pd.concat([sec_data211, data72], ignore_index=True)
    sec_data212 = pd.concat([sec_data212, data73], ignore_index=True)
    sec_data213 = pd.concat([sec_data213, data81], ignore_index=True)
    sec_data214 = pd.concat([sec_data214, data82], ignore_index=True)
    sec_data215 = pd.concat([sec_data215, data83], ignore_index=True)
    #sec_data216 = pd.concat([sec_data216, data91], ignore_index=True)
    #sec_data217 = pd.concat([sec_data217, data92], ignore_index=True)
    #sec_data218 = pd.concat([sec_data218, data93], ignore_index=True)
        


 
sec_data192.to_csv('/home/alex/baikal/files_13/new/sec_data192_13_1')   
sec_data193.to_csv('/home/alex/baikal/files_13/new/sec_data193_13_1')  
sec_data194.to_csv('/home/alex/baikal/files_13/new/sec_data194_13_1')  
sec_data195.to_csv('/home/alex/baikal/files_13/new/sec_data195_13_1')    
sec_data196.to_csv('/home/alex/baikal/files_13/new/sec_data196_13_1')  
sec_data197.to_csv('/home/alex/baikal/files_13/new/sec_data197_13_1')  
sec_data198.to_csv('/home/alex/baikal/files_13/new/sec_data198_13_1')    
sec_data199.to_csv('/home/alex/baikal/files_13/new/sec_data199_13_1')  
sec_data200.to_csv('/home/alex/baikal/files_13/new/sec_data200_13_1') 
sec_data201.to_csv('/home/alex/baikal/files_13/new/sec_data201_13_1')    
sec_data202.to_csv('/home/alex/baikal/files_13/new/sec_data202_13_1')  
sec_data203.to_csv('/home/alex/baikal/files_13/new/sec_data203_13_1') 
sec_data204.to_csv('/home/alex/baikal/files_13/new/sec_data204_13_1')    
sec_data205.to_csv('/home/alex/baikal/files_13/new/sec_data205_13_1')  
sec_data206.to_csv('/home/alex/baikal/files_13/new/sec_data206_13_1') 
sec_data207.to_csv('/home/alex/baikal/files_13/new/sec_data207_13_1')  
sec_data208.to_csv('/home/alex/baikal/files_13/new/sec_data208_13_1') 
sec_data209.to_csv('/home/alex/baikal/files_13/new/sec_data209_13_1')  
sec_data210.to_csv('/home/alex/baikal/files_13/new/sec_data210_13_1')  
sec_data211.to_csv('/home/alex/baikal/files_13/new/sec_data211_13_1')  
sec_data212.to_csv('/home/alex/baikal/files_13/new/sec_data212_13_1')  
sec_data213.to_csv('/home/alex/baikal/files_13/new/sec_data213_13_1')  
sec_data214.to_csv('/home/alex/baikal/files_13/new/sec_data214_13_1')  
sec_data215.to_csv('/home/alex/baikal/files_13/new/sec_data215_13_1')  
#sec_data216.to_csv('sec_data216_10_1')  
#sec_data217.to_csv('sec_data217_10_1')  
#sec_data218.to_csv('sec_data218_10_1')      
print(sec_data197)

        
# построение графиков для каждой секции
'''
    fig1 = plt.figure()
    fig1.set_figheight(30)
    fig1.set_figwidth(25)
    fig1.suptitle(f'{i}')
    ax1 = fig1.add_subplot(331)
    ax1.set_title('Гирлянда 1, 192')
    #ax1.set_xlabel('Time')
    ax1.set_ylabel('сигнал')
    plt.scatter(data11['t'], data11['y'], color = 'black', s=2, marker='*')
    ax2 = fig1.add_subplot(332)
    ax2.set_title('Гирлянда 1, 193')
    #ax2.set_xlabel('Time')
    ax2.set_ylabel('сигнал')
    plt.scatter(data12['t'], data12['y'], color = 'black', s=2, marker='*')
    ax3 = fig1.add_subplot(333)
    ax3.set_title('Гирлянда 1, 194')
    #ax3.set_xlabel('Time')
    ax3.set_ylabel('сигнал')
    plt.scatter(data13['t'], data13['y'], color = 'black', s=2, marker='*')
    ax5 = fig1.add_subplot(334)
    ax5.set_title('Гирлянда 2, 195')
    #ax5.set_xlabel('Time')
    ax5.set_ylabel('сигнал')
    plt.scatter(data21['t'], data21['y'], color = 'black', s=2, marker='*')
    ax4 = fig1.add_subplot(335)
    ax4.set_title('Гирлянда 2, 196')
    #ax4.set_xlabel('Time')
    ax4.set_ylabel('сигнал')
    plt.scatter(data22['t'], data22['y'], color = 'black', s=2, marker='*')
    ax6 = fig1.add_subplot(336)
    ax6.set_title('Гирлянда 2, 197')
    #ax6.set_xlabel('Time')
    ax6.set_ylabel('сигнал')
    plt.scatter(data23['t'], data23['y'], color = 'black', s=2, marker='*')
    ax7 = fig1.add_subplot(337)
    ax7.set_title('Гирлянда 3, 198')
    ax7.set_xlabel('Time')
    ax7.set_ylabel('сигнал')
    plt.scatter(data31['t'], data31['y'], color = 'black', s=2, marker='*')
    ax8 = fig1.add_subplot(338)
    ax8.set_title('Гирлянда 3, 199')
    ax8.set_xlabel('Time')
    ax8.set_ylabel('сигнал')
    plt.scatter(data32['t'], data32['y'], color = 'black', s=2, marker='*')
    ax9 = fig1.add_subplot(339)
    ax9.set_title('Гирлянда 3, 200')
    ax9.set_xlabel('Time')
    ax9.set_ylabel('сигнал')
    plt.scatter(data33['t'], data33['y'], color = 'black', s=2, marker='*')
    #plt.show()
    
    
    fig2 = plt.figure(figsize=(30, 25))
    fig2.suptitle(f'{i}')
    ax1 = fig2.add_subplot(331)
    ax1.set_title('Гирлянда 4, 201')
    #ax1.set_xlabel('Time')
    ax1.set_ylabel('сигнал')
    plt.scatter(data41['t'], data41['y'], color = 'black', s=2, marker='*')
    ax2 = fig2.add_subplot(332)
    ax2.set_title('Гирлянда 4, 202')
    #ax2.set_xlabel('Time')
    ax2.set_ylabel('сигнал')
    plt.scatter(data42['t'], data42['y'], color = 'black', s=2, marker='*')
    ax3 = fig2.add_subplot(333)
    ax3.set_title('Гирлянда 4, 203')
    #ax3.set_xlabel('Time')
    ax3.set_ylabel('сигнал')
    plt.scatter(data43['t'], data43['y'], color = 'black', s=2, marker='*')
    ax5 = fig2.add_subplot(334)
    ax5.set_title('Гирлянда 5, 204')
    #ax5.set_xlabel('Time')
    ax5.set_ylabel('сигнал')
    plt.scatter(data51['t'], data51['y'], color = 'black', s=2, marker='*')
    ax4 = fig2.add_subplot(335)
    ax4.set_title('Гирлянда 5, 205')
    #ax4.set_xlabel('Time')
    ax4.set_ylabel('сигнал')
    plt.scatter(data52['t'], data52['y'], color = 'black', s=2, marker='*')
    ax6 = fig2.add_subplot(336)
    ax6.set_title('Гирлянда 5, 206')
    #ax6.set_xlabel('Time')
    ax6.set_ylabel('сигнал')
    plt.scatter(data53['t'], data53['y'], color = 'black', s=2, marker='*')
    ax7 = fig2.add_subplot(337)
    ax7.set_title('Гирлянда 6, 207')
    ax7.set_xlabel('Time')
    ax7.set_ylabel('сигнал')
    plt.scatter(data61['t'], data61['y'], color = 'black', s=2, marker='*')
    ax8 = fig2.add_subplot(338)
    ax8.set_title('Гирлянда 6, 208')
    ax8.set_xlabel('Time')
    ax8.set_ylabel('сигнал')
    plt.scatter(data62['t'], data62['y'], color = 'black', s=2, marker='*')
    ax9 = fig2.add_subplot(339)
    ax9.set_title('Гирлянда 6, 209')
    ax9.set_xlabel('Time')
    ax9.set_ylabel('сигнал')
    plt.scatter(data63['t'], data63['y'], color = 'black', s=2, marker='*')
    #plt.show()

    fig3 = plt.figure(figsize=(30, 25))
    fig3.suptitle(f'{i}')
    ax1 = fig3.add_subplot(331)
    ax1.set_title('Гирлянда 7, 210')
    #ax1.set_xlabel('Time')
    ax1.set_ylabel('сигнал')
    plt.scatter(data71['t'], data71['y'], color = 'black', s=2, marker='*')
    ax2 = fig3.add_subplot(332)
    ax2.set_title('Гирлянда 7, 211')
    #ax2.set_xlabel('Time')
    ax2.set_ylabel('сигнал')
    plt.scatter(data72['t'], data72['y'], color = 'black', s=2, marker='*')
    ax3 = fig3.add_subplot(333)
    ax3.set_title('Гирлянда 7, 212')
    #ax3.set_xlabel('Time')
    ax3.set_ylabel('сигнал')
    plt.scatter(data73['t'], data73['y'], color = 'black', s=2, marker='*')
    ax5 = fig3.add_subplot(334)
    ax5.set_title('Гирлянда 8, 213')
    #ax5.set_xlabel('Time')
    ax5.set_ylabel('сигнал')
    plt.scatter(data81['t'], data81['y'], color = 'black', s=2, marker='*')
    ax4 = fig3.add_subplot(335)
    ax4.set_title('Гирлянда 8, 214')
    #ax4.set_xlabel('Time')
    ax4.set_ylabel('сигнал')
    plt.scatter(data82['t'], data82['y'], color = 'black', s=2, marker='*')
    ax6 = fig3.add_subplot(336)
    ax6.set_title('Гирлянда 8, 215')
    #ax6.set_xlabel('Time')
    ax6.set_ylabel('сигнал')
    plt.scatter(data83['t'], data83['y'], color = 'black', s=2, marker='*')
    ax7 = fig3.add_subplot(337)
    ax7.set_title('Гирлянда 9, 216')
    ax7.set_xlabel('Time')
    ax7.set_ylabel('сигнал')
    plt.scatter(data91['t'], data91['y'], color = 'black', s=2, marker='*')
    ax8 = fig3.add_subplot(338)
    ax8.set_title('Гирлянда 9, 217')
    ax8.set_xlabel('Time')
    ax8.set_ylabel('сигнал')
    plt.scatter(data92['t'], data92['y'], color = 'black', s=2, marker='*')
    ax9 = fig3.add_subplot(339)
    ax9.set_title('Гирлянда 9, 218')
    ax9.set_xlabel('Time')
    ax9.set_ylabel('сигнал')
    plt.scatter(data93['t'], data93['y'], color = 'black', s=2, marker='*')
    #plt.show()
    
    
    fig1.savefig(f'3strings1_{i}.png')
    fig2.savefig(f'3strings2_{i}.png')
    fig3.savefig(f'3strings3_{i}.png')
'''



    # создание сетки 
    #x = [i for i in range(1, 37)]
    #y = [i for i in range(1, 10)]
    #flux = np.array([x, y])


# какая-то сортровка по амплитуде...
    #print(data['y'].mean())


    #fig1 = plt.figure(figsize=(12, 7))
    #fig1.suptitle(f'{i}')
    #ax1 = fig1.add_subplot(111)
    #ax1.set_title('EXO 040830-7134.7, exptime=20s')
    #ax1.set_xlabel('Time')
    #ax1.set_ylabel('сигнал')
    #plt.scatter(data11['t'], data11['y'], color = 'black', s=5, marker='*')
    #plt.plot(data['t'], data['y'])
    #plt.show()

    #fig1.savefig(f'{name[:42]}0{i}_60.png')

'''
fig2 = plt.figure(figsize=(12, 7))
fig2.suptitle('all')
ax2 = fig2.add_subplot(111)
#ax1.set_title('EXO 040830-7134.7, exptime=20s')
ax2.set_xlabel('Time')
ax2.set_ylabel('сигнал')
plt.scatter(T, Y, color = 'black', s=2, marker='*')
#plt.plot(data['t'], data['y'])
fig2.savefig('10_all.png')
#plt.show()
'''













# этот цикл сильно зависает 
'''
for i in range(len(values)):


    a, b = data_for_plot(values[i], step[i])
    impulse_y.append(a)
    impulse_x.append(b)
    if i > 5000:
        print('done')
        break
    '''
#посмотреть другой способ, этот не работает
#data['impulse_y'], data['impulse_x'] = data['values'].apply(data_for_plot(data['values'], data['step'], False))
#data['impulse_y'], data['impulse_x'] = data_for_plot(data['values'], data['step'], False)


'''
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
'''




end_time = datetime.now()  # время окончания выполнения
execution_time = end_time - start_time  # вычисляем время выполнения
 
print(f"Время выполнения программы: {execution_time}")