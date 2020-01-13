import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import numpy as np
import re
pd.options.mode.chained_assignment = None
url = "https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "lxml")
soup.prettify()
all_tables=soup.find_all("table")

right_table=soup.find_all('table', class_='wikitable collapsible')
#right_table[0] is the right table
rows = right_table[0].find_all('tr')

headers = [th.text for th in rows[0].find_all('th')]
#print(headers)


import pandas as pd
d = pd.DataFrame()
dall = pd.DataFrame()

n=0
for i in range(1,len(rows)-1):
    fields = rows[i].find_all('td')
    #print(i,fields)
    if fields:
        if 'span class="nowrap"' in str(fields) and '<td rowspan="1"><span class="nowrap"' not in str(fields) and ('Operational' in str(rows[i+1].find_all('td')) or 'Successful' in str(rows[i+1].find_all('td')) or 'En route' in str(rows[i+1].find_all('td'))):

            prezzonetto = rows[i].find('span',attrs={'class':'nowrap'}).text
            n=n+1
            #print(prezzonetto)
            temp=pd.DataFrame({'date': '2019 '+prezzonetto, 'no': 1}, index=[0])
            d = pd.concat([d, temp])
        if 'span class="nowrap"' in str(fields) and '<td rowspan="1"><span class="nowrap"' not in str(fields):
            prezzonetto = rows[i].find('span',attrs={'class':'nowrap'}).text
            tempall=pd.DataFrame({'date': '2019 '+re.sub("[\(\[].*?[\)\]]", "",prezzonetto), 'value': 0}, index=[0])
            dall = pd.concat([dall, tempall])
            

            
dall=dall.drop_duplicates()
for i in range(0,len(dall)):
    date_str_de_DE = dall['date'].iloc[i]
    #print(date_str_de_DE)
    datetime_object = datetime.datetime.strptime(re.sub("^\s+|\s+$", "",date_str_de_DE), '%Y %d %B')
    dall['date'].iloc[i]=datetime_object.isoformat()+'+00:00'

dd=d['date'].value_counts()
dd=pd.DataFrame(dd)
dd['value'] = dd.index

for i in range(0,len(dd)):
    date_str_de_DE = dd['value'].iloc[i]
    datetime_object = datetime.datetime.strptime(date_str_de_DE, '%Y %d %B')
    dd['value'].iloc[i]=datetime_object.isoformat()+'+00:00'
dd=dd.sort_values(by='value')

dd = dd[['value', 'date']]
dd.columns = ['date', 'value']

dfinal=dall.merge(dd,how='left', left_on='date', right_on='date')
dfinal = dfinal.replace(np.nan, 0, regex=True)
pd.options.display.float_format = '{:,.0f}'.format
del dfinal['value_x']
dfinal.columns = ['date', 'value']
dfinal.value = dfinal.value.astype(int)
dfinal.value.iloc[83]=0 #this one is ambiguous. I don't know if the we consider this a successful or not. I assumed not successful. 
export_csv = dfinal.to_csv (r'sagef.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path
export_csv
