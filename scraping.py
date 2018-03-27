# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 23:23:29 2018

@author: Bradley Dufour
"""

import pandas as pd
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("Listo de Kontakto.html", encoding="utf8"), "html.parser")

words = soup.html.body.table.tbody.findAll('tr')[1].findAll('td')
categorized = pd.DataFrame(columns=['root','pos','common'])
for td in words:
    column = td.ol.findAll('li')
    for li in column:
        bolded = False;
        if 'style' in li.attrs:
            if(li['style'] == 'font-weight: bold;'):
                bolded = True;
        
        word = li.a
        wordType = 'misc'
        if(word.text[0] == '-'):
            wordType = 'suf'
        elif(word.text[-1] == '-'):
            wordType = 'pre'
        elif(word.text[-1] == 'o'):
            wordType = 'N'
        elif(word.text[-1] == 'a'):
            wordType = 'A'
        elif(word.text[-1] == 'i'):
            if 'style' in word.attrs:
                if(word['style'] == 'color: rgb(255, 0, 0);'):
                    wordType = 'VI'
                elif(word['style'] == 'color: rgb(0, 0, 255)'):
                    wordType = 'VT'
                elif(word['style'] == 'color: rgb(0, 255, 0)'):
                    wordType = 'VTI'
                    
        spelling = word.text
        
        row = pd.DataFrame([[spelling, wordType, bolded]], columns=['root','pos','common'])
        categorized = categorized.append(row)

print(categorized)
categorized.to_csv(path_or_buf='esperanto.csv', encoding='utf8', index=False)