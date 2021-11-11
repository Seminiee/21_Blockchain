# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 13:46:10 2021

@author: dani0
"""
#%%

def make_16byte_form(hexdecimal_string):
    res = ""
    if len(hexdecimal_string) == 16:
        res = hexdecimal_string
    else:
        zero_head = ""
        for j in range(0,16-len(hexdecimal_string)):
            zero_head += '0'
        res = zero_head + hexdecimal_string
    return res

def make_8bit_form(binarized_int_string):
    res = ""
    if len(binarized_int_string) == 8:
        res = binarized_int_string
    else:
        zero_head = ""
        for j in range(0,8-len(binarized_int_string)):
            zero_head += '0'
        res = zero_head + binarized_int_string
    return res

def make_4byte_hex_form(hex_string):
    res = ""
    if len(hex_string) == 8:
        res = hex_string
    else:
        zero_head = ""
        for j in range(0,8-len(hex_string)):
            zero_head += '0'
        res = zero_head + hex_string
    return res
     
def make_8bit_hex_form(hex_string):
    res = ""
    if len(hex_string) == 2:
        res = hex_string
    else:
        res = '0' + hex_string
    return res
    
def aes_128_pre_round(hex_plain,hex_key,sbox):
    RC = ['00000001','00000010','00000100','00001000','00010000',
          '00100000','01000000','10000000','00011011','00110110']
    hex_plain_list = []
    for i in range(16):
        hex_plain_list.append(hex_plain[2*i]+hex_plain[2*i+1])
    hex_plain_mat_rowfirst = list()
    for i in range(4):
        for j in range(4):
            hex_plain_mat_rowfirst.append(hex_plain_list[4*j + i])
    k_list = []
    for i in range(4):
        k_list.append(hex_key[8*i:8*(i+1)])
    pre_round = []
    W=["" for x in range(44)]
    for i in range(4):
        W[i] = k_list[i]
    for i in range(4,44):
        if i % 4 == 0:
            sub_word = []
            for j in range(4):
                sub_word.append(W[i-1][2*j:2*(j+1)])
            sub_word1 = make_8bit_hex_form(hex(int(sbox[int(sub_word[1],16)],16) ^ int(RC[i//4-1],2))[2:]) 
            sub_word2 = make_8bit_hex_form(hex(int(sbox[int(sub_word[2],16)],16))[2:])
            sub_word3 = make_8bit_hex_form(hex(int(sbox[int(sub_word[3],16)],16))[2:])
            sub_word0 = make_8bit_hex_form(hex(int(sbox[int(sub_word[0],16)],16))[2:])
            w_i = make_4byte_hex_form(hex(int(sub_word1 + sub_word2 + sub_word3 + sub_word0,16) ^ int(W[i-4],16))[2:])
        else:
            w_i = make_4byte_hex_form(hex(int(W[i-1],16) ^ int(W[i-4],16))[2:])
        
        W[i] = w_i
    key_xor = []
    for i in range(4):
        for j in range(4):
            key_xor.append(W[j][2*i:2*(i+1)])
    for i in range(16):
        pr = make_8bit_hex_form(hex(int(hex_plain_mat_rowfirst[i],16) ^ int(key_xor[i],16))[2:])
        pre_round.append(pr)
    return (pre_round,W)
 

def aes_128_mid(round_end,sbox,W,round_idx):
    sub_bytes = []
    tmp_list = []
    idx = 0
    for i in round_end:
        tmp_list.append(sbox[int(i,16)])
        if idx % 4 == 3:
            sub_bytes.append(tmp_list)
            tmp_list = []
        idx += 1
    sub_bytes_copied = sub_bytes.copy()
    idx = 0
    shift_rows = [["","","",""],
                 ["","","",""],
                 ["","","",""],
                 ["","","",""]]

    for i in range(4):
        for idx,j in enumerate(range(i,4)):
            shift_rows[i][idx] = sub_bytes_copied[i][j]
        for j in range(0,i):
            idx += 1
            shift_rows[i][idx] = sub_bytes_copied[i][j]
    #mix_columns_mat = [['02','03','01','01'],['01', '02', '03', '01'],['01', '01', '02', '03'],['03', '01', '01', '02']]
    mix_columns_mat = ['02','03','01','01','01', '02', '03', '01','01', '01', '02', '03','03', '01', '01', '02']
    #col_idx = 0
    #mix_cols_cal = []
    for i in range(4):
    #col_indices = [k*4 + i for k in range(4)]
        len_4_list = []
        mixcol = [shift_rows[x][i] for x in range(4)]
        for j in range(16):
            #tmp = make_8bit_form(bin(int(shift_rows[j % 4][i],16))[2:])
            tmp = make_8bit_form(bin(int(mixcol[j % 4],16))[2:])
            if mix_columns_mat[j] == '01':
                tmp_app = int(tmp,2)
            elif mix_columns_mat[j] == '02':
                if tmp[0] == '0':
                    tmp_app = int(tmp[1:] + '0',2)
                else:
                    tmp_app = int(tmp[1:] + '0',2) ^ int('00011011',2)
            else:
                if tmp[0] == '0':
                    tmp_app = int(tmp[1:] + '0',2)
                else:
                    tmp_app = int(tmp[1:] + '0',2) ^ int('00011011',2)
                tmp_app = tmp_app ^ int(tmp,2)
            #print('j: ',j, 'j%4: ', j%4, mix_columns_mat[j], ' ', tmp, make_8bit_form(bin(tmp_app)[2:]))
            len_4_list.append(tmp_app)
            if j % 4 == 3:
                app = len_4_list[0] ^ len_4_list[1] ^ len_4_list[2] ^ len_4_list[3]
                hex_form_app = make_8bit_hex_form(hex(app)[2:])
                sub_bytes_copied[j // 4][i] = hex_form_app
                #print('j: ',j)
                #print(len_4_list)
                len_4_list = list()
    
    cur_round_end = []
    key_xor = []
    for i in range(4):
        for j in range(4*round_idx,4*(round_idx + 1)):
            key_xor.append(W[j][2*i:2*(i+1)])
    for i in range(16):
        pr = make_8bit_hex_form(hex(int(sub_bytes_copied[i//4][i%4],16) ^ int(key_xor[i],16))[2:])
        cur_round_end.append(pr)
    return cur_round_end 
            
def aes_128_last_round(round_end,sbox,W,round_idx):
    sub_bytes = []
    tmp_list = []
    idx = 0
    for i in round_end:
        tmp_list.append(sbox[int(i,16)])
        if idx % 4 == 3:
            sub_bytes.append(tmp_list)
            tmp_list = []
        idx += 1
    sub_bytes_copied = sub_bytes.copy()
    idx = 0
    shift_rows = [["","","",""],
                 ["","","",""],
                 ["","","",""],
                 ["","","",""]]
    for i in range(4):
        for idx,j in enumerate(range(i,4)):
            shift_rows[i][idx] = sub_bytes_copied[i][j]
        for j in range(0,i):
            idx += 1
            shift_rows[i][idx] = sub_bytes_copied[i][j]
    cur_round_end = []
    key_xor = []
    for i in range(4):
        for j in range(4*round_idx,4*(round_idx + 1)):
            key_xor.append(W[j][2*i:2*(i+1)])
    for i in range(16):
        pr = make_8bit_hex_form(hex(int(shift_rows[i//4][i%4],16) ^ int(key_xor[i],16))[2:])
        cur_round_end.append(pr)
    return cur_round_end
        
def aes_128(hex_plain,hex_key,sbox):
    hex_cipher = ""
    pre_round,W = aes_128_pre_round(hex_plain,hex_key,sbox)
    hex_cipher_list = pre_round.copy()
    for i in range(1,10):
        hex_cipher_list = aes_128_mid(hex_cipher_list,sbox,W,i)
    hex_cipher_list = aes_128_last_round(hex_cipher_list,sbox,W,10)
    cipher_indices = [0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15]
    for i in cipher_indices:
        hex_cipher += hex_cipher_list[i]
    return hex_cipher
#%%
#sample inputs and outputs

sbox = ['63', '7c',	'77',	'7b',	'f2',	'6b',	'6f',	'c5',	'30',	'01',	'67',	'2b',	'fe',	'd7',	'ab',	'76',
        'ca', '82',	'c9',	'7d',	'fa',	'59',	'47',	'f0',	'ad',	'd4',	'a2',	'af',	'9c',	'a4',	'72',	'c0',
        'b7', 'fd',	'93',	'26',	'36',	'3f',	'f7',	'cc',	'34',	'a5',	'e5',	'f1',	'71',	'd8',	'31',	'15',
        '04', 'c7',	'23',	'c3',	'18',	'96',	'05',	'9a',	'07',	'12',	'80',	'e2',	'eb',	'27',	'b2',	'75',
        '09', '83',	'2c',	'1a',	'1b',	'6e',	'5a',	'a0',	'52',	'3b',	'd6',	'b3',	'29',	'e3',	'2f',	'84',
        '53', 'd1',	'00',	'ed',	'20',	'fc',	'b1',	'5b',	'6a',	'cb',	'be',	'39',	'4a',	'4c',	'58',	'cf',
        'd0', 'ef',	'aa',	'fb',	'43',	'4d',	'33',	'85',	'45',	'f9',	'02',	'7f',	'50',	'3c',	'9f',	'a8',
        '51', 'a3',	'40',	'8f',	'92',	'9d',	'38',	'f5',	'bc',	'b6',	'da',	'21',	'10',	'ff',	'f3',	'd2',
        'cd', '0c',	'13',	'ec',	'5f',	'97',	'44',	'17',	'c4',	'a7',	'7e',	'3d',	'64',	'5d',	'19',	'73',
        '60', '81',	'4f',	'dc',	'22',	'2a',	'90',	'88',	'46',	'ee',	'b8',	'14',	'de',	'5e',	'0b',	'db',
        'e0', '32',	'3a',	'0a',	'49',	'06',	'24',	'5c',	'c2',	'd3',	'ac',	'62',	'91',	'95',	'e4',	'79',
        'e7', 'c8',	'37',	'6d',	'8d',	'd5',	'4e',	'a9',	'6c',	'56',	'f4',	'ea',	'65',	'7a',	'ae',	'08',
        'ba', '78',	'25',	'2e',	'1c',	'a6',	'b4',	'c6',	'e8',	'dd',	'74',	'1f',	'4b',	'bd',	'8b',	'8a',
        '70', '3e',	'b5',	'66',	'48',	'03',	'f6',	'0e',	'61',	'35',	'57',	'b9',	'86',	'c1',	'1d',	'9e',
        'e1', 'f8',	'98',	'11',	'69',	'd9',	'8e',	'94',	'9b',	'1e',	'87',	'e9',	'ce',	'55',	'28',	'df',
        '8c', 'a1',	'89',	'0d',	'bf',	'e6',	'42',	'68',	'41',	'99',	'2d',	'0f',	'b0',	'54',	'bb',	'16']

'''
sample_input_plaintext = '3abba72027afc6d01d50968badaf52ba'
sample_input_key = '3cfa0397225b46dbdee7a5a171238c5c'
sample_output = 'ef22fe11ddd6d200b0685f35c14f4fad'
'''

sample_input_plaintext = '51dc3136ecf5b6e3cddf27008850b48d'
sample_input_key = '488ae3726b88953fa3a70854ef1faefa'
sample_output = '27654e1c78373788e82cf5fe5dd2e0e3'


'''
sample_input_plaintext = '4e4c2e7dd8d83034e3fce5a7a6c2d399'
sample_input_key = '9875dbedc80f3b0bc2163135a2485a96'
sample_output = '597e93e163be4092a1490861a5cb3faf'
'''

'''
sample_input_plaintext = 'e39db08efd8131f86f0f0e5f9e18f342'
sample_input_key = '900fbab2f494297459814e5a8ea25070'
sample_output = '56e4c69d6b354be2dafae0671b77689c'
'''

my_output = aes_128(sample_input_plaintext,sample_input_key,sbox)
print(my_output == sample_output)
#%%
#input

sbox = ['63', '7c',	'77',	'7b',	'f2',	'6b',	'6f',	'c5',	'30',	'01',	'67',	'2b',	'fe',	'd7',	'ab',	'76',
        'ca', '82',	'c9',	'7d',	'fa',	'59',	'47',	'f0',	'ad',	'd4',	'a2',	'af',	'9c',	'a4',	'72',	'c0',
        'b7', 'fd',	'93',	'26',	'36',	'3f',	'f7',	'cc',	'34',	'a5',	'e5',	'f1',	'71',	'd8',	'31',	'15',
        '04', 'c7',	'23',	'c3',	'18',	'96',	'05',	'9a',	'07',	'12',	'80',	'e2',	'eb',	'27',	'b2',	'75',
        '09', '83',	'2c',	'1a',	'1b',	'6e',	'5a',	'a0',	'52',	'3b',	'd6',	'b3',	'29',	'e3',	'2f',	'84',
        '53', 'd1',	'00',	'ed',	'20',	'fc',	'b1',	'5b',	'6a',	'cb',	'be',	'39',	'4a',	'4c',	'58',	'cf',
        'd0', 'ef',	'aa',	'fb',	'43',	'4d',	'33',	'85',	'45',	'f9',	'02',	'7f',	'50',	'3c',	'9f',	'a8',
        '51', 'a3',	'40',	'8f',	'92',	'9d',	'38',	'f5',	'bc',	'b6',	'da',	'21',	'10',	'ff',	'f3',	'd2',
        'cd', '0c',	'13',	'ec',	'5f',	'97',	'44',	'17',	'c4',	'a7',	'7e',	'3d',	'64',	'5d',	'19',	'73',
        '60', '81',	'4f',	'dc',	'22',	'2a',	'90',	'88',	'46',	'ee',	'b8',	'14',	'de',	'5e',	'0b',	'db',
        'e0', '32',	'3a',	'0a',	'49',	'06',	'24',	'5c',	'c2',	'd3',	'ac',	'62',	'91',	'95',	'e4',	'79',
        'e7', 'c8',	'37',	'6d',	'8d',	'd5',	'4e',	'a9',	'6c',	'56',	'f4',	'ea',	'65',	'7a',	'ae',	'08',
        'ba', '78',	'25',	'2e',	'1c',	'a6',	'b4',	'c6',	'e8',	'dd',	'74',	'1f',	'4b',	'bd',	'8b',	'8a',
        '70', '3e',	'b5',	'66',	'48',	'03',	'f6',	'0e',	'61',	'35',	'57',	'b9',	'86',	'c1',	'1d',	'9e',
        'e1', 'f8',	'98',	'11',	'69',	'd9',	'8e',	'94',	'9b',	'1e',	'87',	'e9',	'ce',	'55',	'28',	'df',
        '8c', 'a1',	'89',	'0d',	'bf',	'e6',	'42',	'68',	'41',	'99',	'2d',	'0f',	'b0',	'54',	'bb',	'16']
hex_Plaintext = input()
hex_Key = input()

cipher = aes_128(hex_Plaintext,hex_Key,sbox)
print(cipher)



#%%























































