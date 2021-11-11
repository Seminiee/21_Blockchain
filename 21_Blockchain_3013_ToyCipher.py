# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 20:56:14 2021

@author: dani0
"""
#%%

plain = input()
key = input()
#print('plain: ', plain)
#print('key: ', key)
#%%

sbox = [232, 226,  52, 242, 220, 198, 199, 237,  57, 164,   0,  63,  70, 211, 222, 137,

        62,   59,   2, 171,  77,  12,  71, 177,  83,   7, 102,  64,  75, 170, 153,  98,

        190,  36, 241, 154, 238,  39,  30, 244, 172,  50,  73,  82,  87, 145, 181, 176,

        245, 125,  31, 173, 253,  27,  17, 138, 122, 135,   5, 156, 113,  28, 118, 105,

        107, 168,   3, 225, 217, 243, 229,  19,  20,  18, 223, 109, 108, 123,  78,  96,

        208,  14, 130, 240,  97, 104, 174,  88,  58, 103, 194, 110,  81,  94,  43,  49,

        114, 139,  44, 132, 115, 142, 140, 106, 197, 169, 117,  24, 165,  29,  41, 188,

        162, 134,  15, 191, 157, 163, 231, 207,  46,  10,   8, 116,  23, 111,  74,  25,

        206,  99,   1,  11, 175, 246,  45, 200, 192,  60, 189,  90, 148, 143,  40,   6,

        69,  218, 121,  26, 100,  80, 152, 250, 179, 228, 214, 161,  34, 203, 213, 193,

        89,  204,  21, 221, 205, 233,  76, 249, 230,  51, 227, 147,  53, 149, 182, 196,

        9,    72,  47,  48, 248, 186, 167,  66, 202, 160, 183,  95,  79,  91,  32, 234,

        68,   85,  22,  67, 239, 120, 180, 150, 201, 124, 184, 178, 235,  93, 252, 216,

        127, 101,  54, 158,  55,  33, 128, 136,  61,  92,  56, 255, 187,  84, 254, 126,

        159, 185, 236, 151, 247, 141,  16, 251,  65, 209, 131, 166,   4,  35, 215, 133,

        146, 144, 224, 119,  37,  38,  86, 212, 210, 129,  13,  42, 155, 112, 219, 195]


#%%


#%%
#Test Cell

sample_input1 = '84bd5f9c'
sample_input1_skey = '12345678'
sample_output1 = '583b545e'

sample_input2 = 'fedfdfc1'
sample_input2_skey = 'f1f2f3f4'
sample_output2 = 'e81fd9ed'

sample_input3 = '1597def3'
sample_input3_skey = '49ce26dd'
sample_output3 = '3d2588ec'

sample_input4 = '777481c9'
sample_input4_skey = '96de15c3'
sample_output4 = '7bf941f5'

#%%

def make_32bit_form(binarized_int_string):
    res = ""
    if len(binarized_int_string) == 32:
        res = binarized_int_string
    else:
        zero_head = ""
        zero_head = ""
        for j in range(0,32-len(binarized_int_string)):
            zero_head += '0'
        res = zero_head + binarized_int_string
    return res

#%%
find_right_rotation = bin(int('7e7212f5',16))[2:]
print(find_right_rotation,len(find_right_rotation)) #1111110011100100001001011110101 31

#%%
find_right_rotation = make_32bit_form(bin(int('7e7212f5',16))[2:]) #'01111110011100100001001011110101'
bin_sample_input1 = '10000100101111010101111110011100'
for i in range(1,32):
    x = bin_sample_input1[-i:]
    y = bin_sample_input1[:-i]
    right_rotate = x + y
    
    if find_right_rotation == right_rotate: #14
        print(i)

#%%

def make_32bit_form(binarized_int_string):
    res = ""
    if len(binarized_int_string) == 32:
        res = binarized_int_string
    else:
        zero_head = ""
        zero_head = ""
        for j in range(0,32-len(binarized_int_string)):
            zero_head += '0'
        res = zero_head + binarized_int_string
    return res

def make_8bit_hex_form(hex_string):
    res = ""
    if len(hex_string) == 2:
        res = hex_string
    else:
        res = '0' + hex_string
    return res

def toyCipher(plaintext,key_hex,right_rotate_bit,sbox):
    bin_plaintext = make_32bit_form(bin(int(plaintext,16))[2:])
    x = bin_plaintext[-right_rotate_bit:]
    y = bin_plaintext[:-right_rotate_bit]
    right_rotated_p = x + y
    for_sbox_list = []
    
    for i in range(4):
        tmp = right_rotated_p[8*i:8*(i+1)]
        if i==3:
            tmp = right_rotated_p[8*i:]
        for_sbox_list.append(sbox[int(tmp,2)])
    encryption = ""
    for i in for_sbox_list:
        hex_part = make_8bit_hex_form(hex(i)[2:])
        encryption += hex_part
    xor_res = int(encryption,16) ^ int(key_hex,16)
    hex_xor_res = hex(xor_res)[2:]
    cipher = hex_xor_res
    if len(hex_xor_res) < 8 :
        zero_head = ""
        for i in range(0,8-len(hex_xor_res)):
            zero_head += "0"
        cipher = zero_head + hex_xor_res
    
    return cipher
        

plain = input()
key = input()

sbox = [232, 226,  52, 242, 220, 198, 199, 237,  57, 164,   0,  63,  70, 211, 222, 137,

        62,   59,   2, 171,  77,  12,  71, 177,  83,   7, 102,  64,  75, 170, 153,  98,

        190,  36, 241, 154, 238,  39,  30, 244, 172,  50,  73,  82,  87, 145, 181, 176,

        245, 125,  31, 173, 253,  27,  17, 138, 122, 135,   5, 156, 113,  28, 118, 105,

        107, 168,   3, 225, 217, 243, 229,  19,  20,  18, 223, 109, 108, 123,  78,  96,

        208,  14, 130, 240,  97, 104, 174,  88,  58, 103, 194, 110,  81,  94,  43,  49,

        114, 139,  44, 132, 115, 142, 140, 106, 197, 169, 117,  24, 165,  29,  41, 188,

        162, 134,  15, 191, 157, 163, 231, 207,  46,  10,   8, 116,  23, 111,  74,  25,

        206,  99,   1,  11, 175, 246,  45, 200, 192,  60, 189,  90, 148, 143,  40,   6,

        69,  218, 121,  26, 100,  80, 152, 250, 179, 228, 214, 161,  34, 203, 213, 193,

        89,  204,  21, 221, 205, 233,  76, 249, 230,  51, 227, 147,  53, 149, 182, 196,

        9,    72,  47,  48, 248, 186, 167,  66, 202, 160, 183,  95,  79,  91,  32, 234,

        68,   85,  22,  67, 239, 120, 180, 150, 201, 124, 184, 178, 235,  93, 252, 216,

        127, 101,  54, 158,  55,  33, 128, 136,  61,  92,  56, 255, 187,  84, 254, 126,

        159, 185, 236, 151, 247, 141,  16, 251,  65, 209, 131, 166,   4,  35, 215, 133,

        146, 144, 224, 119,  37,  38,  86, 212, 210, 129,  13,  42, 155, 112, 219, 195]

ans = toyCipher(plain,key,14,sbox)
print(ans)

#print(ans == sample_output4)




#%%








