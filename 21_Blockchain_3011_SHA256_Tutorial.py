# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 19:14:28 2021

@author: dani0
"""

#%%
'''
Description
    주어진 문자열을 입력받아, sha-256 hash 결과값을 산출하는 프로그램을 작성하시오.

    (단, 모든 입력 데이터와 출력 데이터의 형태는 숫자와 알파벳 소문자만을 사용함.)
    
Step-by-step SHA-256 hash

Step1 - Pre-processing
'''



#%%

def preProcessing_Padding(inputValue):
    binary_converted_string_list = list()
    #Convert inputValue to binary
    for i in inputValue:
        tmp = bin(ord(i))
        if i == ' ':
            tmp = tmp.replace('b','0')
        tmp = tmp.replace('b','')
        binary_converted_string_list.append(tmp)
    bin_inputValue_length = len(binary_converted_string_list) * 8
    
    #Padding
    binary_converted_string_list.append('10000000')
    first_loop = 8 - len(binary_converted_string_list) % 8
    for i in range(0, first_loop):
        binary_converted_string_list.append('00000000')
    second_loop = (448 - len(binary_converted_string_list) * 8) // 64
    
    for i in range(0,second_loop):
        binary_converted_string_list += ['00000000','00000000','00000000','00000000','00000000','00000000','00000000','00000000']
    binary_converted_string_list +=['00000000','00000000','00000000','00000000','00000000','00000000','00000000']
    tmp = bin(bin_inputValue_length).replace('b','')
    binary_converted_string_list.append(tmp)
    
    return binary_converted_string_list

def chunk_and_create_Message_Schedule_Loop(preProcessed_list):
    chunkList = list()
    tmp = ""
    for i in range(len(preProcessed_list)):
        tmp += preProcessed_list[i]
        if i % 4 == 3:
            chunkList.append(tmp)
            tmp = ""
    chunkList_tmp_len = len(chunkList)
    #for i in range(chunkList_tmp_len, 64):
        #chunkList.append('00000000000000000000000000000000')
    
    for i in range(chunkList_tmp_len, 64):
        a = chunkList[i-15][-7:]
        b = chunkList[i-15][:-7]
        rightrotate7 = a + b
        
        a = chunkList[i-15][-18:]
        b = chunkList[i-15][:-18]
        rightrotate18 = a + b
        
        a = '000'
        b = chunkList[i-15][:-3]
        rightshift3 = a + b
        
        s0 = int(rightrotate7,2) ^ int(rightrotate18,2) ^ int(rightshift3,2) 
        
        a = chunkList[i-2][-17:]
        b = chunkList[i-2][:-17]
        rightrotate17 = a + b
        
        a = chunkList[i-2][-19:]
        b = chunkList[i-2][:-19]
        rightrotate19 = a + b
        
        a = '0000000000'
        b = chunkList[i-2][:-10]
        rightshift10 = a + b
        
        s1 = int(rightrotate17,2) ^ int(rightrotate19,2) ^ int(rightshift10,2)
        w_i = int(chunkList[i-16],2) + s0 + int(chunkList[i-7],2) + s1
        
        while(True):
            if w_i < 4294967296:
                break
            else:
                w_i -= 4294967296
                
        binary_w_i = bin(w_i)[2:]
        if len(binary_w_i) < 32:
            head_zero_string = ""
            for i in range(0,32-len(binary_w_i)):
                head_zero_string += '0'
            binary_w_i = head_zero_string + binary_w_i
        chunkList.append(binary_w_i)
        
    return chunkList

'''
def create_Message_Schedule(chunked_list, chunked_list_len):
    message_list = chunked_list.copy()
    
    for i in range(chunked_list_len,len(chunked_list)):
        a = message_list[i-15][-7:]
        b = message_list[i-15][:-7]
        rightrotate7 = a + b
        
        a = message_list[i-15][-18:]
        b = message_list[i-15][:-18]
        rightrotate18 = a + b
        
        a = '000'
        b = message_list[i-15][:-3]
        rightshift3 = a + b
        
        s0 = int(rightrotate7,2) ^ int(rightrotate18,2) ^ int(rightshift3,2)
        
        a = message_list[i-2][-17:]
        b = message_list[i-2][:-17]
        rightrotate17 = a + b
        a = message_list[i-2][-19:]
        b = message_list[i-2][:-19]
        rightrotate19 = a + b
        a = '0000000000'
        b = message_list[i-2][:-10]
        rightshift10 = a + b
        
        s1 = int(rightrotate17,2) ^ int(rightrotate19,2) ^ int(rightshift10,2)
        w_i = int(chunked_list[i-16],2) + s0 + int(chunked_list[i-7],2) + s1
        
        while(True):
            if w_i < 4294967296:
                break
            else:
                w_i -= 4294967296
                
        binary_w_i = bin(w_i)[2:]
        if len(binary_w_i) < 32:
            head_zero_string = ""
            for i in range(0,32-len(binary_w_i)):
                head_zero_string += '0'
        binary_w_i = head_zero_string + binary_w_i
        message_list[i] = binary_w_i
    
    return message_list
'''
#%%
'''
a = test_chunk[1][-7:]
b = test_chunk[1][:-7]
rightrotate7 = a + b
a = test_chunk[1][-18:]
b = test_chunk[1][:-18]
rightrotate18 = a + b
a = '000'
b = test_chunk[1][:-3]
rightshift3 = a + b

s0 = int(rightrotate7,2) ^ int(rightrotate18,2) ^ int(rightshift3,2)
#print(bin(s0))

a = test_chunk[14][-17:]
b = test_chunk[14][:-17]
rightrotate17 = a + b
a = test_chunk[14][-19:]
b = test_chunk[14][:-19]
rightrotate19 = a + b
a = '000'
b = test_chunk[14][:-10]
rightshift10 = a + b

s1 = int(rightrotate17,2) ^ int(rightrotate19,2) ^ int(rightshift10,2)
#print(bin(s1))
forModulo232 = 4294967296
#modulo232 = '11111111111111111111111111111111'
w16 = int(test_chunk[0],2) + s0 + int(test_chunk[9],2) + s1
if w16 >= forModulo232:
    w16 -= forModulo232

print(bin(w16)[2:])
binary_w16 = bin(w16)[2:]
if len(binary_w16) < 32:
    head_zero_string = ""
    for i in range(0,32-len(binary_w16)):
        head_zero_string += '0'
binary_w16 = head_zero_string + binary_w16
print(binary_w16)
'''
#%%

#print(preProcessing('hello world'))
test = preProcessing_Padding('hello world')
#print(test)
#%%

hash_values = {'h0': 0x6a09e667, 'h1': 0xbb67ae85, 'h2': 0x3c6ef372, 'h3': 0xa54ff53a, 
               'h4': 0x510e527f, 'h5': 0x9b05688c, 'h6': 0x1f83d9ab, 'h7': 0x5be0cd19 }

round_constants = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
                   0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
                   0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
                   0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
                   0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
                   0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
                   0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
                   0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]

round_constants_str = ['0x428a2f98','0x71374491','0xb5c0fbcf','0xe9b5dba5','0x3956c25b','0x59f111f1','0x923f82a4','0xab1c5ed5',
                       '0xd807aa98','0x12835b01','0x243185be','0x550c7dc3','0x72be5d74','0x80deb1fe','0x9bdc06a7','0xc19bf174',
                       '0xe49b69c1','0xefbe4786','0x0fc19dc6','0x240ca1cc','0x2de92c6f','0x4a7484aa','0x5cb0a9dc','0x76f988da',
                       '0x983e5152','0xa831c66d','0xb00327c8','0xbf597fc7','0xc6e00bf3','0xd5a79147','0x06ca6351','0x14292967',
                       '0x27b70a85','0x2e1b2138','0x4d2c6dfc','0x53380d13','0x650a7354','0x766a0abb','0x81c2c92e','0x92722c85',
                       '0xa2bfe8a1','0xa81a664b','0xc24b8b70','0xc76c51a3','0xd192e819','0xd6990624','0xf40e3585','0x106aa070',
                       '0x19a4c116','0x1e376c08','0x2748774c','0x34b0bcb5','0x391c0cb3','0x4ed8aa4a','0x5b9cca4f','0x682e6ff3',
                       '0x748f82ee','0x78a5636f','0x84c87814','0x8cc70208','0x90befffa','0xa4506ceb','0xbef9a3f7','0xc67178f2']

test_chunk = chunk_and_create_Message_Schedule_Loop(test)

#print(test_chunk)

#%%

binary_hash_values = list()
for i in hash_values:
    tmp = bin(hash_values[i])[2:]
    if len(tmp) < 32:
        zero_head = ""
        for j in range(0,32-len(tmp)):
            zero_head += '0'
        binary_hash_values.append(zero_head+tmp)
    else:
        binary_hash_values.append(tmp)
        
a = binary_hash_values[0]
b = binary_hash_values[1]
c = binary_hash_values[2]
d = binary_hash_values[3]
e = binary_hash_values[4]
f = binary_hash_values[5]
g = binary_hash_values[6]
h = binary_hash_values[7]

#%%
x = e[-6:]
y = e[:-6]
e_rightrotate_6 = x+y
print(e_rightrotate_6)
#%%
x = e[-11:]
y = e[:-11]
e_rightrotate_11 = x+y
print(e_rightrotate_11)
#%%
x = e[-25:]
y = e[:-25]
e_rightrotate_25 = x+y
print(e_rightrotate_25)
#%%
s1 = bin(int(e_rightrotate_6,2) ^ int(e_rightrotate_11,2) ^ int(e_rightrotate_25,2))[2:]
if len(s1) < 32:
    zero_head = ""
    for j in range(0,32-len(s1)):
        zero_head += '0'
    tmp = s1
    s1 = ""
    s1 = zero_head + tmp

ch = bin((int(e,2) & int(f,2)) ^ ((~int(e,2)) & int(g,2)))[2:]
if len(ch) <32:
    zero_head = ""
    for j in range(0,32-len(ch)):
        zero_head += '0'
    tmp = ch
    ch = ""
    ch = zero_head + tmp

temp1_int = int(h,2) + int(s1,2) +int(ch,2) + int(round_constants_str[0],16) + int(test_chunk[0],2)
while(True):
    if temp1_int < 4294967296:
        break
    else:
        temp1_int -= 4294967296
temp1 = bin(temp1_int)[2:]
if len(temp1) < 32:
    zero_head = ""
    for j in range(0,32-len(temp1)):
        zero_head += '0'
    mv_tmp = temp1
    temp1 = ""
    temp1 = zero_head + mv_tmp
print(temp1)

#%%
x = a[-2:]
y = a[:-2]
a_rightrotate_2 = x+y
print(a_rightrotate_2)
#%%
x = a[-13:]
y = a[:-13]
a_rightrotate_13 = x+y
print(a_rightrotate_13)
#%%
x = a[-22:]
y = a[:-22]
a_rightrotate_22 = x+y
print(a_rightrotate_22)

#%%
s0_int = int(a_rightrotate_2,2) ^ int(a_rightrotate_13,2) ^ int(a_rightrotate_22,2)
s0 = bin(s0_int)[2:]

#%%

maj_int = (int(a,2) & int(b,2)) ^ (int(a,2) & int(c,2)) ^ (int(b,2) & int(c,2))
if len(bin(maj_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(maj_int)[2:])):
        zero_head += '0'
    maj = zero_head + bin(maj_int)[2:]
print(maj)

#%%

temp2_int = int(s0,2) + int(maj,2)
while(True):
    if temp2_int < 4294967296:
        break
    else:
        temp2_int -= 4294967296
if len(bin(temp2_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(temp2_int)[2:])):
        zero_head += '0'
    temp2 = zero_head + bin(temp2_int)[2:]
print(temp2)

#%%
h = g
g = f
f = e
e_int = int(d,2) + int(temp1,2)
while(True):
    if e_int < 4294967296:
        break
    else:
        e_int -= 4294967296
if len(bin(e_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(e_int)[2:])):
        zero_head += '0'
    e = zero_head + bin(e_int)[2:]
d = c
c = b
b = a
a_int = int(temp1,2) + int(temp2,2)
while(True):
    if a_int < 4294967296:
        break
    else:
        a_int -= 4294967296
if len(bin(a_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(a_int)[2:])):
        zero_head += '0'
    a = zero_head + bin(a_int)[2:]
print(h == '00011111100000111101100110101011')
print(g == '10011011000001010110100010001100')
print(f == '01010001000011100101001001111111')
print(e == '00000001001011010100111100001110')
print(d == '00111100011011101111001101110010')
print(c == '10111011011001111010111010000101')
print(b == '01101010000010011110011001100111')
print(a == '01100100011011011111010010111001')



#%%

for i in range(0,64):
    x = e[-6:]
    y = e[:-6]
    e_rightrotate_6 = x+y
    
    x = e[-11:]
    y = e[:-11]
    e_rightrotate_11 = x+y
    
    x = e[-25:]
    y = e[:-25]
    e_rightrotate_25 = x+y
    
    s1 = bin(int(e_rightrotate_6,2) ^ int(e_rightrotate_11,2) ^ int(e_rightrotate_25,2))[2:]
    if len(s1) < 32:
        zero_head = ""
        for j in range(0,32-len(s1)):
            zero_head += '0'
        tmp = s1
        s1 = ""
        s1 = zero_head + tmp
    
    ch = bin((int(e,2) & int(f,2)) ^ ((~int(e,2)) & int(g,2)))[2:]
    if len(ch) <32:
        zero_head = ""
        for j in range(0,32-len(ch)):
            zero_head += '0'
        tmp = ch
        ch = ""
        ch = zero_head + tmp
    
    temp1_int = int(h,2) + int(s1,2) +int(ch,2) + round_constants[i] + int(test_chunk[i],2)
    while(True):
        if temp1_int < 4294967296:
            break
        else:
            temp1_int -= 4294967296
    temp1 = bin(temp1_int)[2:]
    if len(temp1) < 32:
        zero_head = ""
        for j in range(0,32-len(temp1)):
            zero_head += '0'
        mv_tmp = temp1
        temp1 = ""
        temp1 = zero_head + mv_tmp

    x = a[-2:]
    y = a[:-2]
    a_rightrotate_2 = x+y

    x = a[-13:]
    y = a[:-13]
    a_rightrotate_13 = x+y

    x = a[-22:]
    y = a[:-22]
    a_rightrotate_22 = x+y
    
    s0_int = int(a_rightrotate_2,2) ^ int(a_rightrotate_13,2) ^ int(a_rightrotate_22,2)
    #s0 = bin(s0_int)[2:]
    
    maj_int = (int(a,2) & int(b,2)) ^ (int(a,2) & int(c,2)) ^ (int(b,2) & int(c,2))
    '''
    if len(bin(maj_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(maj_int)[2:])):
            zero_head += '0'
        maj = zero_head + bin(maj_int)[2:]
    '''
    temp2_int = s0_int + maj_int
    temp2_int = temp2_int % 4294967296
    
    '''
    if len(bin(temp2_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(temp2_int)[2:])):
            zero_head += '0'
        temp2 = zero_head + bin(temp2_int)[2:]
    '''
    h = g
    g = f
    f = e
    e_int = int(d,2) + int(temp1,2)
    e_int = e_int % 4294967296
    e = bin(e_int)[2:]
    if len(bin(e_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(e_int)[2:])):
            zero_head += '0'
        e = zero_head + bin(e_int)[2:]
    d = c
    c = b
    b = a
    a_int = int(temp1,2) + temp2_int
    a_int = a_int % 4294967296
    a = bin(a_int)[2:]
    if len(bin(a_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(a_int)[2:])):
            zero_head += '0'
        a = zero_head + bin(a_int)[2:]
#%%

print(a)
print(b)
print(c)
print(d)
print(e)
print(f)
print(g)
print(h)
#%%

h0_int = hash_values['h0'] + int(a,2)
h0_int = h0_int % 4294967296
if len(bin(h0_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(h0_int)[2:])):
        zero_head += '0'
    h0 = zero_head + bin(h0_int)[2:]
else:
    h0 = bin(h0_int)[2:]
        
h1_int = hash_values['h1'] + int(b,2)
h1_int = h1_int % 4294967296
if len(bin(h1_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(h1_int)[2:])):
        zero_head += '0'
    h1 = zero_head + bin(h1_int)[2:]
else:
    h1 = bin(h1_int)[2:]
        
h2_int = hash_values['h2'] + int(c,2)
h2_int = h2_int % 4294967296
if len(bin(h2_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(h2_int)[2:])):
        zero_head += '0'
    h2 = zero_head + bin(h2_int)[2:]
else:
    h2 = bin(h2_int)[2:]

h3_int = hash_values['h3'] + int(d,2)
h3_int = h3_int % 4294967296
if len(bin(h3_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(h3_int)[2:])):
        zero_head += '0'
    h3 = zero_head + bin(h3_int)[2:]
else:
    h3 = bin(h3_int)[2:]

h4_int = hash_values['h4'] + int(e,2)
h4_int = h4_int % 4294967296
if len(bin(h4_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(h4_int)[2:])):
        zero_head += '0'
    h4 = zero_head + bin(h4_int)[2:]
else:
    h4 = bin(h4_int)[2:]

h5_int = hash_values['h5'] + int(f,2)
h5_int = h5_int % 4294967296
if len(bin(h5_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(h5_int)[2:])):
        zero_head += '0'
    h5 = zero_head + bin(h5_int)[2:]
else:
    h5 = bin(h5_int)[2:]

h6_int = hash_values['h6'] + int(g,2)
h6_int = h6_int % 4294967296
if len(bin(h6_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(h6_int)[2:])):
        zero_head += '0'
    h6 = zero_head + bin(h6_int)[2:]
else:
    h6 = bin(h6_int)[2:]

h7_int = hash_values['h7'] + int(h,2)
h7_int = h7_int % 4294967296
if len(bin(h7_int)[2:]) < 32:
    zero_head = ""
    for j in range(0,32-len(bin(h7_int)[2:])):
        zero_head += '0'
    h7 = zero_head + bin(h7_int)[2:]
else:
    h7 = bin(h7_int)[2:]
#%%
'''
h0_int = hash_values['h0'] + int(a,2)
while(True):
    h0_int = h0_int % 4294967296
    if h0_int < 4294967296:
        break
    else:
        h0_int -= 4294967296
    if len(bin(h0_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(h0_int)[2:])):
            zero_head += '0'
        h0 = zero_head + bin(h0_int)[2:]
        
h1_int = hash_values['h1'] + int(b,2)
while(True):
    if h1_int < 4294967296:
        break
    else:
        h0_int -= 4294967296
    if len(bin(h0_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(h1_int)[2:])):
            zero_head += '0'
        h1 = zero_head + bin(h1_int)[2:]
        
h2_int = hash_values['h2'] + int(c,2)
while(True):
    if h2_int < 4294967296:
        break
    else:
        h2_int -= 4294967296
    if len(bin(h2_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(h2_int)[2:])):
            zero_head += '0'
        h2 = zero_head + bin(h2_int)[2:]

h3_int = hash_values['h3'] + int(d,2)
while(True):
    if h3_int < 4294967296:
        break
    else:
        h3_int -= 4294967296
    if len(bin(h3_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(h3_int)[2:])):
            zero_head += '0'
        h3 = zero_head + bin(h3_int)[2:]

h4_int = hash_values['h4'] + int(e,2)
while(True):
    if h4_int < 4294967296:
        break
    else:
        h4_int -= 4294967296
    if len(bin(h4_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(h4_int)[2:])):
            zero_head += '0'
        h4 = zero_head + bin(h4_int)[2:]

h5_int = hash_values['h5'] + int(f,2)
while(True):
    if h5_int < 4294967296:
        break
    else:
        h5_int -= 4294967296
    if len(bin(h5_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(h5_int)[2:])):
            zero_head += '0'
        h5 = zero_head + bin(h5_int)[2:]

h6_int = hash_values['h6'] + int(g,2)
while(True):
    if h6_int < 4294967296:
        break
    else:
        h6_int -= 4294967296
    if len(bin(h6_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(h6_int)[2:])):
            zero_head += '0'
        h6 = zero_head + bin(h6_int)[2:]

h7_int = hash_values['h7'] + int(h,2)
while(True):
    if h7_int < 4294967296:
        break
    else:
        h7_int -= 4294967296
    if len(bin(h7_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(h7_int)[2:])):
            zero_head += '0'
        h7 = zero_head + bin(h7_int)[2:]
'''
#%%
digest = hex(int(h0,2))[2:] + hex(int(h1,2))[2:] + hex(int(h2,2))[2:] + hex(int(h3,2))[2:] + hex(int(h4,2))[2:] + hex(int(h5,2))[2:] + hex(int(h6,2))[2:] + hex(int(h7,2))[2:]
print(digest.lower())

#%%

digest = hex(h0_int)[2:] + hex(h1_int)[2:] + hex(h2_int)[2:] + hex(h3_int)[2:] + hex(h4_int)[2:] + hex(h5_int)[2:] + hex(h6_int)[2:] + hex(h7_int)[2:]
print(digest.lower())
#%%
'''
import numpy as np

message_schedule_answer = np.array(['01101000011001010110110001101100', '01101111001000000111011101101111',
                                    '01110010011011000110010010000000', '00000000000000000000000000000000',
                                    '00000000000000000000000000000000', '00000000000000000000000000000000',
                                    '00000000000000000000000000000000', '00000000000000000000000000000000',
                                    '00000000000000000000000000000000', '00000000000000000000000000000000',
                                    '00000000000000000000000000000000', '00000000000000000000000000000000',
                                    '00000000000000000000000000000000', '00000000000000000000000000000000',
                                    '00000000000000000000000000000000', '00000000000000000000000001011000',
                                    '00110111010001110000001000110111', '10000110110100001100000000110001',
                                    '11010011101111010001000100001011', '01111000001111110100011110000010',
                                    '00101010100100000111110011101101', '01001011001011110111110011001001',
                                    '00110001111000011001010001011101', '10001001001101100100100101100100',
                                    '01111111011110100000011011011010', '11000001011110011010100100111010',
                                    '10111011111010001111011001010101', '00001100000110101110001111100110',
                                    '10110000111111100000110101111101', '01011111011011100101010110010011',
                                    '00000000100010011001101101010010', '00000111111100011100101010010100',
                                    '00111011010111111110010111010110', '01101000011001010110001011100110',
                                    '11001000010011100000101010011110', '00000110101011111001101100100101',
                                    '10010010111011110110010011010111', '01100011111110010101111001011010',
                                    '11100011000101100110011111010111', '10000100001110111101111000010110',
                                    '11101110111011001010100001011011', '10100000010011111111001000100001',
                                    '11111001000110001010110110111000', '00010100101010001001001000011001',
                                    '00010000100001000101001100011101', '01100000100100111110000011001101',
                                    '10000011000000110101111111101001', '11010101101011100111100100111000',
                                    '00111001001111110000010110101101', '11111011010010110001101111101111',
                                    '11101011011101011111111100101001', '01101010001101101001010100110100',
                                    '00100010111111001001110011011000', '10101001011101000000110100101011',
                                    '01100000110011110011100010000101', '11000100101011001001100000111010',
                                    '00010001010000101111110110101101', '10110000101100000001110111011001',
                                    '10011000111100001100001101101111', '01110010000101111011100000011110',
                                    '10100010110101000110011110011010', '00000001000011111001100101111011',
                                    '11111100000101110100111100001010', '11000010110000101110101100010110'])

nparraytmp = np.array(test_chunk)

print(len(message_schedule_answer == nparraytmp))
'''


#%%

#For CIS Online Judge Problem 3011 Submission

sample_output1 = 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9' #hello world
#sample_output1 = '22f350c1e89a4a53ffdf66172e6ff43b6cc420d9d324b26de158950cf2cafb27' #yeppiyeppi

def preProcessing_Padding(inputValue):
    binary_converted_string_list = list()
    #Convert inputValue to binary
    for i in inputValue:
        tmp = bin(ord(i))
        if i == ' ':
            tmp = tmp.replace('b','0')
        tmp = tmp.replace('b','')
        binary_converted_string_list.append(tmp)
    bin_inputValue_length = len(binary_converted_string_list) * 8
    
    #Padding
    binary_converted_string_list.append('10000000')
    first_loop = 8 - len(binary_converted_string_list) % 8
    for i in range(0, first_loop):
        binary_converted_string_list.append('00000000')
    second_loop = (448 - len(binary_converted_string_list) * 8) // 64
    
    for i in range(0,second_loop):
        binary_converted_string_list += ['00000000','00000000','00000000','00000000','00000000','00000000','00000000','00000000']
    binary_converted_string_list +=['00000000','00000000','00000000','00000000','00000000','00000000','00000000']
    tmp = bin(bin_inputValue_length).replace('b','')
    binary_converted_string_list.append(tmp)
    
    return binary_converted_string_list

def chunk_and_create_Message_Schedule_Loop(preProcessed_list):
    chunkList = list()
    tmp = ""
    for i in range(len(preProcessed_list)):
        tmp += preProcessed_list[i]
        if i % 4 == 3:
            chunkList.append(tmp)
            tmp = ""
    chunkList_tmp_len = len(chunkList)
    
    for i in range(chunkList_tmp_len, 64):
        a = chunkList[i-15][-7:]
        b = chunkList[i-15][:-7]
        rightrotate7 = a + b
        
        a = chunkList[i-15][-18:]
        b = chunkList[i-15][:-18]
        rightrotate18 = a + b
        
        a = '000'
        b = chunkList[i-15][:-3]
        rightshift3 = a + b
        
        s0 = int(rightrotate7,2) ^ int(rightrotate18,2) ^ int(rightshift3,2) 
        
        a = chunkList[i-2][-17:]
        b = chunkList[i-2][:-17]
        rightrotate17 = a + b
        
        a = chunkList[i-2][-19:]
        b = chunkList[i-2][:-19]
        rightrotate19 = a + b
        
        a = '0000000000'
        b = chunkList[i-2][:-10]
        rightshift10 = a + b
        
        s1 = int(rightrotate17,2) ^ int(rightrotate19,2) ^ int(rightshift10,2)
        w_i = int(chunkList[i-16],2) + s0 + int(chunkList[i-7],2) + s1
        
        while(True):
            if w_i < 4294967296:
                break
            else:
                w_i -= 4294967296
                
        binary_w_i = bin(w_i)[2:]
        if len(binary_w_i) < 32:
            head_zero_string = ""
            for i in range(0,32-len(binary_w_i)):
                head_zero_string += '0'
            binary_w_i = head_zero_string + binary_w_i
        chunkList.append(binary_w_i)
        
    return chunkList

input_string = input()
test = preProcessing_Padding(input_string)

hash_values = {'h0': 0x6a09e667, 'h1': 0xbb67ae85, 'h2': 0x3c6ef372, 'h3': 0xa54ff53a, 
               'h4': 0x510e527f, 'h5': 0x9b05688c, 'h6': 0x1f83d9ab, 'h7': 0x5be0cd19 }

round_constants = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
                   0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
                   0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
                   0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
                   0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
                   0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
                   0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
                   0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]

test_chunk = chunk_and_create_Message_Schedule_Loop(test)

binary_hash_values = list()
for i in hash_values:
    tmp = bin(hash_values[i])[2:]
    if len(tmp) < 32:
        zero_head = ""
        for j in range(0,32-len(tmp)):
            zero_head += '0'
        binary_hash_values.append(zero_head+tmp)
    else:
        binary_hash_values.append(tmp)
        
a = binary_hash_values[0]
b = binary_hash_values[1]
c = binary_hash_values[2]
d = binary_hash_values[3]
e = binary_hash_values[4]
f = binary_hash_values[5]
g = binary_hash_values[6]
h = binary_hash_values[7]

for i in range(0,64):
    x = e[-6:]
    y = e[:-6]
    e_rightrotate_6 = x+y
    
    x = e[-11:]
    y = e[:-11]
    e_rightrotate_11 = x+y
    
    x = e[-25:]
    y = e[:-25]
    e_rightrotate_25 = x+y
    
    s1 = bin(int(e_rightrotate_6,2) ^ int(e_rightrotate_11,2) ^ int(e_rightrotate_25,2))[2:]
    if len(s1) < 32:
        zero_head = ""
        for j in range(0,32-len(s1)):
            zero_head += '0'
        tmp = s1
        s1 = ""
        s1 = zero_head + tmp
    
    ch = bin((int(e,2) & int(f,2)) ^ ((~int(e,2)) & int(g,2)))[2:]
    if len(ch) <32:
        zero_head = ""
        for j in range(0,32-len(ch)):
            zero_head += '0'
        tmp = ch
        ch = ""
        ch = zero_head + tmp
    
    temp1_int = int(h,2) + int(s1,2) +int(ch,2) + round_constants[i] + int(test_chunk[i],2)
    while(True):
        if temp1_int < 4294967296:
            break
        else:
            temp1_int -= 4294967296
    temp1 = bin(temp1_int)[2:]
    if len(temp1) < 32:
        zero_head = ""
        for j in range(0,32-len(temp1)):
            zero_head += '0'
        mv_tmp = temp1
        temp1 = ""
        temp1 = zero_head + mv_tmp

    x = a[-2:]
    y = a[:-2]
    a_rightrotate_2 = x+y

    x = a[-13:]
    y = a[:-13]
    a_rightrotate_13 = x+y

    x = a[-22:]
    y = a[:-22]
    a_rightrotate_22 = x+y
    
    s0_int = int(a_rightrotate_2,2) ^ int(a_rightrotate_13,2) ^ int(a_rightrotate_22,2)
    
    maj_int = (int(a,2) & int(b,2)) ^ (int(a,2) & int(c,2)) ^ (int(b,2) & int(c,2))
    
    temp2_int = s0_int + maj_int
    temp2_int = temp2_int % 4294967296
    
    h = g
    g = f
    f = e
    e_int = int(d,2) + int(temp1,2)
    e_int = e_int % 4294967296
    e = bin(e_int)[2:]
    if len(bin(e_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(e_int)[2:])):
            zero_head += '0'
        e = zero_head + bin(e_int)[2:]
    d = c
    c = b
    b = a
    a_int = int(temp1,2) + temp2_int
    a_int = a_int % 4294967296
    a = bin(a_int)[2:]
    if len(bin(a_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(a_int)[2:])):
            zero_head += '0'
        a = zero_head + bin(a_int)[2:]

h0_int = hash_values['h0'] + int(a,2)
h0_int = h0_int % 4294967296

h1_int = hash_values['h1'] + int(b,2)
h1_int = h1_int % 4294967296

h2_int = hash_values['h2'] + int(c,2)
h2_int = h2_int % 4294967296

h3_int = hash_values['h3'] + int(d,2)
h3_int = h3_int % 4294967296

h4_int = hash_values['h4'] + int(e,2)
h4_int = h4_int % 4294967296

h5_int = hash_values['h5'] + int(f,2)
h5_int = h5_int % 4294967296

h6_int = hash_values['h6'] + int(g,2)
h6_int = h6_int % 4294967296

h7_int = hash_values['h7'] + int(h,2)
h7_int = h7_int % 4294967296

#digest = ""
digest = hex(h0_int) + hex(h1_int)[2:] + hex(h2_int)[2:] + hex(h3_int)[2:] + hex(h4_int)[2:] + hex(h5_int)[2:] + hex(h6_int)[2:] + hex(h7_int)[2:]

print(format(int(digest,16),'x'))
print(digest)
print(int(digest,16))
#print(digest == sample_output1)

#%%

def preProcessing_Padding(inputValue):
    binary_converted_string_list = list()
    #Convert inputValue to binary
    for i in inputValue:
        tmp = bin(ord(i))
        if i == ' ':
            tmp = tmp.replace('b','0')
        tmp = tmp.replace('b','')
        binary_converted_string_list.append(tmp)
    bin_inputValue_length = len(binary_converted_string_list) * 8
    
    #Padding
    binary_converted_string_list.append('10000000')
    first_loop = 8 - len(binary_converted_string_list) % 8
    for i in range(0, first_loop):
        binary_converted_string_list.append('00000000')
    second_loop = (448 - len(binary_converted_string_list) * 8) // 64
    
    for i in range(0,second_loop):
        binary_converted_string_list += ['00000000','00000000','00000000','00000000','00000000','00000000','00000000','00000000']
    binary_converted_string_list +=['00000000','00000000','00000000','00000000','00000000','00000000','00000000']
    tmp = bin(bin_inputValue_length).replace('b','')
    binary_converted_string_list.append(tmp)
    
    return binary_converted_string_list

def chunk_and_create_Message_Schedule_Loop(preProcessed_list):
    chunkList = list()
    tmp = ""
    for i in range(len(preProcessed_list)):
        tmp += preProcessed_list[i]
        if i % 4 == 3:
            chunkList.append(tmp)
            tmp = ""
    chunkList_tmp_len = len(chunkList)
    
    for i in range(chunkList_tmp_len, 64):
        a = chunkList[i-15][-7:]
        b = chunkList[i-15][:-7]
        rightrotate7 = a + b
        
        a = chunkList[i-15][-18:]
        b = chunkList[i-15][:-18]
        rightrotate18 = a + b
        
        a = '000'
        b = chunkList[i-15][:-3]
        rightshift3 = a + b
        
        s0 = int(rightrotate7,2) ^ int(rightrotate18,2) ^ int(rightshift3,2) 
        
        a = chunkList[i-2][-17:]
        b = chunkList[i-2][:-17]
        rightrotate17 = a + b
        
        a = chunkList[i-2][-19:]
        b = chunkList[i-2][:-19]
        rightrotate19 = a + b
        
        a = '0000000000'
        b = chunkList[i-2][:-10]
        rightshift10 = a + b
        
        s1 = int(rightrotate17,2) ^ int(rightrotate19,2) ^ int(rightshift10,2)
        w_i = int(chunkList[i-16],2) + s0 + int(chunkList[i-7],2) + s1
        
        while(True):
            if w_i < 4294967296:
                break
            else:
                w_i -= 4294967296
                
        binary_w_i = bin(w_i)[2:]
        if len(binary_w_i) < 32:
            head_zero_string = ""
            for i in range(0,32-len(binary_w_i)):
                head_zero_string += '0'
            binary_w_i = head_zero_string + binary_w_i
        chunkList.append(binary_w_i)
        
    return chunkList

input_string = input()
target_round = int(input())
test = preProcessing_Padding(input_string)

hash_values = {'h0': 0x6a09e667, 'h1': 0xbb67ae85, 'h2': 0x3c6ef372, 'h3': 0xa54ff53a, 
               'h4': 0x510e527f, 'h5': 0x9b05688c, 'h6': 0x1f83d9ab, 'h7': 0x5be0cd19 }

round_constants = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
                   0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
                   0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
                   0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
                   0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
                   0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
                   0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
                   0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]

test_chunk = chunk_and_create_Message_Schedule_Loop(test)

binary_hash_values = list()
for i in hash_values:
    tmp = bin(hash_values[i])[2:]
    if len(tmp) < 32:
        zero_head = ""
        for j in range(0,32-len(tmp)):
            zero_head += '0'
        binary_hash_values.append(zero_head+tmp)
    else:
        binary_hash_values.append(tmp)
        
a = binary_hash_values[0]
b = binary_hash_values[1]
c = binary_hash_values[2]
d = binary_hash_values[3]
e = binary_hash_values[4]
f = binary_hash_values[5]
g = binary_hash_values[6]
h = binary_hash_values[7]

for i in range(0,target_round):
    x = e[-6:]
    y = e[:-6]
    e_rightrotate_6 = x+y
    
    x = e[-11:]
    y = e[:-11]
    e_rightrotate_11 = x+y
    
    x = e[-25:]
    y = e[:-25]
    e_rightrotate_25 = x+y
    
    s1 = bin(int(e_rightrotate_6,2) ^ int(e_rightrotate_11,2) ^ int(e_rightrotate_25,2))[2:]
    if len(s1) < 32:
        zero_head = ""
        for j in range(0,32-len(s1)):
            zero_head += '0'
        tmp = s1
        s1 = ""
        s1 = zero_head + tmp
    
    ch = bin((int(e,2) & int(f,2)) ^ ((~int(e,2)) & int(g,2)))[2:]
    if len(ch) <32:
        zero_head = ""
        for j in range(0,32-len(ch)):
            zero_head += '0'
        tmp = ch
        ch = ""
        ch = zero_head + tmp
    
    temp1_int = int(h,2) + int(s1,2) +int(ch,2) + round_constants[i] + int(test_chunk[i],2)
    while(True):
        if temp1_int < 4294967296:
            break
        else:
            temp1_int -= 4294967296
    temp1 = bin(temp1_int)[2:]
    if len(temp1) < 32:
        zero_head = ""
        for j in range(0,32-len(temp1)):
            zero_head += '0'
        mv_tmp = temp1
        temp1 = ""
        temp1 = zero_head + mv_tmp

    x = a[-2:]
    y = a[:-2]
    a_rightrotate_2 = x+y

    x = a[-13:]
    y = a[:-13]
    a_rightrotate_13 = x+y

    x = a[-22:]
    y = a[:-22]
    a_rightrotate_22 = x+y
    
    s0_int = int(a_rightrotate_2,2) ^ int(a_rightrotate_13,2) ^ int(a_rightrotate_22,2)
    
    maj_int = (int(a,2) & int(b,2)) ^ (int(a,2) & int(c,2)) ^ (int(b,2) & int(c,2))
    
    temp2_int = s0_int + maj_int
    temp2_int = temp2_int % 4294967296
    
    h = g
    g = f
    f = e
    e_int = int(d,2) + int(temp1,2)
    e_int = e_int % 4294967296
    e = bin(e_int)[2:]
    if len(bin(e_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(e_int)[2:])):
            zero_head += '0'
        e = zero_head + bin(e_int)[2:]
    d = c
    c = b
    b = a
    a_int = int(temp1,2) + temp2_int
    a_int = a_int % 4294967296
    a = bin(a_int)[2:]
    if len(bin(a_int)[2:]) < 32:
        zero_head = ""
        for j in range(0,32-len(bin(a_int)[2:])):
            zero_head += '0'
        a = zero_head + bin(a_int)[2:]

hex_a = hex(int(a,2))[2:]
print(hex_a)
#%%



























