# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 13:46:10 2021

@author: dani0
"""
#%%

def make_16byte_form(hexdecimal_string):
    '''
    출력값을 16byte(128bit)의 16진수 string으로 하기 위해
    (앞자릿수가 0이면 python은 출력을 하지 않기 때문에)
    Parameters
    ----------
    hexdecimal_string : string
        16진수 문자열! 앞에 '0x'가 붙어있으면 인식x
        hex(int_value)[2:] 나 format() 사용 가능
    Returns
    -------
    res : string
        16byte(128bit)의 16진수 string
        len(res) = 32
    '''
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
    '''
    출력값을 8bit의 2진수 string으로 하기 위해
    (앞자릿수가 0이면 python은 출력을 하지 않기 때문에)
    Parameters
    ----------
    binarized_int_string : string
        2진수 문자열! 앞에 '0b'가 붙어있으면 인식x
        bin(int_value)[2:] 나 format() 사용 가능
    Returns
    -------
    res : string
        8bit의 2진수 string
        len(res) = 8
    '''
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
    '''
    출력값을 4byte(32bit)의 16진수 string으로 하기 위해
    (앞자릿수가 0이면 python은 출력을 하지 않기 때문에)
    Parameters
    ----------
    hex_string : string
        16진수 문자열! 앞에 '0x'가 붙어있으면 인식x
        hex(int_value)[2:] 나 format() 사용 가능
    Returns
    -------
    res : string
        4byte(32bit)의 16진수 string
        len(res) = 8
    '''
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
    '''
    출력값을 8bit의 16진수 string으로 하기 위해
    (앞자릿수가 0이면 python은 0을 출력을 하지 않기 때문에)
    Parameters
    ----------
    hex_string : string
        16진수 문자열! 앞에 '0x'가 붙어있으면 인식x
        hex(int_value)[2:] 나 format() 사용 가능
    Returns
    -------
    res : string
        8bit의 16진수 string
        len(res) = 2
    '''
    res = ""
    if len(hex_string) == 2:
        res = hex_string
    else:
        res = '0' + hex_string
    return res
    
def aes_128_pre_round(hex_plain,hex_key,sbox):
    '''
    AES의 pre_round 단계로, 키 xor 연산만 진행
    키 xor 연산 후 결과 list와, key expansion한 결과 리턴
    Parameters
    ----------
    hex_plain : 16진수 string ('0x' 접두어 없음)
        16진수 평문
    hex_key : 16진수 string ('0x' 접두어 없음)
        16진수 key
    sbox : List
        Substitution Box, 길이는 256, 요소 하나하나는 1byte 16진수 string

    Returns
    -------
    pre_round : List
        평문을 Pre_round 진행 후 상태의 1차원 list
    W : list
        len(W) = 44
        Key Expansion 한 결과값

    '''
    #Round Constant
    RC = ['00000001','00000010','00000100','00001000','00010000',
          '00100000','01000000','10000000','00011011','00110110']
    
    #1byte 단위로 평문 분할
    hex_plain_list = []
    for i in range(16):
        hex_plain_list.append(hex_plain[2*i]+hex_plain[2*i+1])
        
    #AES 알고리즘에서 column 먼저 채우는 형태의 matrix 사용 그냥 1차원 배열로 사용하는 것.
    hex_plain_mat_colfirst = list()
    for i in range(4):
        for j in range(4):
            hex_plain_mat_colfirst.append(hex_plain_list[4*j + i])
    k_list = []
    for i in range(4):
        k_list.append(hex_key[8*i:8*(i+1)])
    pre_round = []
    
    #Key Expansion 진행
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
    
    #현재 round에서 사용할 키 추출(pre_round는 입력값으로 받은 key 그대로 사용)
    key_xor = []
    for i in range(4):
        for j in range(4):
            key_xor.append(W[j][2*i:2*(i+1)])
    for i in range(16):
        pr = make_8bit_hex_form(hex(int(hex_plain_mat_colfirst[i],16) ^ int(key_xor[i],16))[2:])
        pre_round.append(pr)
    return (pre_round,W)
 

def aes_128_mid(round_end,sbox,W,round_idx):
    '''
    AES 알고리즘 1round부터 9round까지는 과정이 같음
    1 - SubBytes(S-Box)
    2 - ShiftRows 1행 그대로, 
                  2행은 rotate over 1 bytes(가장 왼쪽 한개가 가장 오른쪽으로), 
                  3행은 rotate over 2 bytes(가장 왼쪽 두개가 가장 오른쪽 2개로), 
                  4행은 rotate over 3 bytes
    3 - MixColumns 
    02 03 01 01
    01 02 03 01
    01 01 02 03
    03 01 01 02
    SubBytes -> ShiftRows -> MixColumns -> AddRoundKey

    Parameters
    ----------
    round_end : 1차원 List
        알고싶은 round의 이전 round 종료 후 결과 .
    sbox : List
        Substitution Box, 길이는 256, 요소 하나하나는 1byte 16진수 string
    W : list
        len(W) = 44
        Key Expansion 한 결과값
    round_idx : int
        구하고 싶은 round

    Returns
    -------
    cur_round_end : 1차원 List
        알고싶은 round의 종료 후 결과 .

    '''
    #SubBytes 단계
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
    
    #ShiftRows 단계
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
            
    #MixColumns 단계
    mix_columns_mat = ['02','03','01','01','01', '02', '03', '01','01', '01', '02', '03','03', '01', '01', '02']
    for i in range(4):
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
    
    #AddRoundkey 단계
    key_xor = []
    for i in range(4):
        for j in range(4*round_idx,4*(round_idx + 1)):
            key_xor.append(W[j][2*i:2*(i+1)])
    for i in range(16):
        pr = make_8bit_hex_form(hex(int(sub_bytes_copied[i//4][i%4],16) ^ int(key_xor[i],16))[2:])
        cur_round_end.append(pr)
    return cur_round_end 
            
def aes_128_last_round(round_end,sbox,W,round_idx):
    '''
    AES 알고리즘 10round는 mixcolumns 단계 없음
    1 - SubBytes(S-Box)
    2 - ShiftRows 1행 그대로, 
                  2행은 rotate over 1 bytes(가장 왼쪽 한개가 가장 오른쪽으로), 
                  3행은 rotate over 2 bytes(가장 왼쪽 두개가 가장 오른쪽 2개로), 
                  4행은 rotate over 3 bytes
    
    SubBytes -> ShiftRows -> AddRoundKey

    Parameters
    ----------
    round_end : 1차원 List
        알고싶은 round의 이전 round 종료 후 결과 .
    sbox : List
        Substitution Box, 길이는 256, 요소 하나하나는 1byte 16진수 string
    W : list
        len(W) = 44
        Key Expansion 한 결과값
    round_idx : int
        구하고 싶은 round
        이 코드는 평문과 키가 모두 128bit인 것만 진행 round_idx = 10

    Returns
    -------
    cur_round_end : 1차원 List
        알고싶은 round의 종료 후 결과 .

    '''
    
    #SubBytes 단계
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
    
    #ShiftRows 단계
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
    
    #AddRoundkey 단계
    key_xor = []
    for i in range(4):
        for j in range(4*round_idx,4*(round_idx + 1)):
            key_xor.append(W[j][2*i:2*(i+1)])
    for i in range(16):
        pr = make_8bit_hex_form(hex(int(shift_rows[i//4][i%4],16) ^ int(key_xor[i],16))[2:])
        cur_round_end.append(pr)
    return cur_round_end
       
def aes_128(hex_plain,hex_key,sbox):
    '''
    aes_128 전체 과정

    Parameters
    ----------
    hex_plain : 16진수 string ('0x' 접두어 없음)
        16진수 평문
    hex_key : 16진수 string ('0x' 접두어 없음)
        16진수 key
    sbox : List
        Substitution Box, 길이는 256, 요소 하나하나는 1byte 16진수 string

    Returns
    -------
    hex_cipher : 16byte hex string
        결과 암호문 string

    '''
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
#제출용 main 코드

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























































