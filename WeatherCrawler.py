
# coding: utf-8

# In[1]:

Location=[
['Taipei', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46692.htm']],
['Keelung', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46694.htm']],
['Taoyuan', ['https://www.cwb.gov.tw/V7/observe/24real/Data/C0C48.htm']],
['Hsinchu', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46757.htm']],
['Miaoli', ['https://www.cwb.gov.tw/V7/observe/24real/Data/C0E75.htm']],
['Taichung', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46749.htm']],
['Nantou', ['https://www.cwb.gov.tw/V7/observe/24real/Data/C0H95.htm']],
['Yunlin', ['https://www.cwb.gov.tw/V7/observe/24real/Data/72K22.htm']],
['Chiayi', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46748.htm']],
['Tainan', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46741.htm']],
['Kaohsiung', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46744.htm']],
['Pingtung', ['https://www.cwb.gov.tw/V7/observe/24real/Data/C0R17.htm']],
['Ilan', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46708.htm']],
['Hualien', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46699.htm']],
['Taitung', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46766.htm']],
['Wuhu', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46735.htm']],
['Quemoy', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46711.htm']],
['Matsu', ['https://www.cwb.gov.tw/V7/observe/24real/Data/46799.htm']]
]


# In[2]:

import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[3]:

# 抓當天時間 做核對用
import datetime


# In[4]:


time = list()
today = datetime.datetime.now() #today()
today.month 
today.day
today.hour

#只留小時 後面+00 
DATE = (str(today.month)+"/"+str(today.day))
TIME = (str(today.hour)+":00")


# In[6]:

# 把時間存進splite

import sqlite3
conn = sqlite3.connect('Temp.sqlite')
cursor = conn.cursor()
cursor.execute('INSERT INTO  "Loc_Temp" ("Date","Time")VALUES (\'' + DATE + '\',\'' + TIME + '\');')
conn.commit()
conn.close()


# In[7]:
# 爬蟲主程式
# 只回傳18個地點前24小時最高氣溫
def Weather(url):
    Loc_page = requests.get(url)
    Loc_page.encoding = 'utf-8'
    Loc = BeautifulSoup(Loc_page.text, 'html.parser')
    Temp = Loc.find_all('td',{'class':"temp1"})
    temp = pd.Series()

    for i in Temp :
        temp = temp.append(pd.Series([i.text])).reset_index(drop=True)
    Hot_temp = max(temp) # 最高溫 若刪除則會存全部的溫度
    return (Hot_temp)


# In[8]:

#地點一一丟進涵式
Temp_list = list()
for loc in Location:
    Temp_list.append((Weather(''.join(loc[1]))))


# In[9]:

#把溫度list內容一一存到 sqlite 選擇時間為最新的row
import sqlite3
conn = sqlite3.connect('Temp.sqlite')
cursor = conn.cursor()

cursor.execute('UPDATE "Loc_Temp" SET "Taipei" = (\'' + Temp_list[0] + '\'), "Keelung" = (\'' + Temp_list[1] + '\'),"Taoyuan" = (\'' + Temp_list[2] + '\'),"Hsinchu" = (\'' + Temp_list[3] + '\'),"Miaoli" = (\'' + Temp_list[4] + '\'), "Taichung" = (\'' + Temp_list[5] + '\'),"Nantou" = (\'' + Temp_list[6] + '\'), "Yunlin" = (\'' + Temp_list[7] + '\'),"Chiayi" = (\'' + Temp_list[8] + '\'),"Tainan" = (\'' + Temp_list[9] + '\'),"Kaohsiung" = (\'' + Temp_list[10] + '\'), "Pingtung" = (\'' + Temp_list[11] + '\'), "Ilan" = (\'' + Temp_list[12] + '\'), "Hualien" = (\'' + Temp_list[13] + '\'), "Taitung" = (\'' + Temp_list[14] + '\'),"Wuhu" = (\'' + Temp_list[15] + '\'),"Quemoy" = (\'' + Temp_list[16] + '\'),"Matsu" = (\'' + Temp_list[17] + '\') WHERE rowid = (SELECT MAX(rowid) FROM Loc_Temp)  ;')

conn.commit()
conn.close()


# In[ ]:



