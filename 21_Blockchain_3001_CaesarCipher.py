# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 13:22:57 2021

@author: dani0
"""

#%%
c,k = input().split(" ")

k = int(k)
alphabet_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
                 'n','o','p','q','r','s','t','u','v','w','x','y','z']

curr_alphabetIndex = 0
p = ""
for curr_alphabet in c:
    curr_alphabetIndex = ord(curr_alphabet) - ord('a')
    plainIndex = (curr_alphabetIndex - k) % 26
    p += alphabet_list[plainIndex]
    
print(p)

#%%