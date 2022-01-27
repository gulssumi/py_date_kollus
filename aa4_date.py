# -*- coding: utf-8 -*- 

import bs4
import requests
import http
import io
import time
#import datetime
from datetime import datetime , timedelta
import os
import csv
import pandas as pd

from Check_Chromedriver import Check_Chromedriver

Check_Chromedriver.driver_mother_path = "c:\down\chromedriver.exe"
Check_Chromedriver.main()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from csv import reader


usr = ""
pwd = ""

path = "c:\down\chromedriver.exe"

# Kollus site login proc
options = webdriver.ChromeOptions()
#options.add_argument("headless")

file_down_path = "c:\\down" # c 드라이브 


options.add_experimental_option("prefs", {
    "download.default_directory": file_down_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})


driver = webdriver.Chrome(path, chrome_options=options)
driver.get("http://www.python.org")

#driver = webdriver.Chrome(path)

driver.get("https://kr.kollus.com/account/signin")
elem = driver.find_element_by_name("account[email]")
elem.send_keys(usr)
elem = driver.find_element_by_name("account[password]")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)

# csv select start , end date 
# 고정 날짜
#s_dt = "2019-11-28"
#e_dt = "2019-12-06"

#s_date = datetime.date(2019,11,28)
#e_date = datetime.date(2019,12,06)

# 자동 날짜 (시작 : 오늘 - 8 종료 : 오늘 -1)
#s_dt = datetime.now() + timedelta(days=-60)
s_dt = datetime.now() + timedelta(days=-15)
e_dt = datetime.now() + timedelta(days=0)

s_date = datetime.date(s_dt)
e_date = datetime.date(e_dt)

s_dt = str(s_dt)[:10]
e_dt = str(e_dt)[:10]

diff = e_date - s_date
#print(diff.days)


b4 = [["3116","megalawers",False],["1612","megals",False],["6870","megamd",False],["7625","megaland",False],["6874","megamdnp",False],["7475","megapsat",False],["7073","mdcamp6",True],["7075","mdcamp7",True],["7081","mdcamp8",True],["7079","mdcamp9",True],["7071","mdcamp13",True],["7077","mdcamp15",True],["7095","mdcamp17",True],["7097","mdcamp18",True],["9863","megassam",False],["10619","megaexpert",False]]
b5 = [[""]*50 for i in range(80)]

def fnGetKollusData(site_ord):
    provider_id = "0"
    site_name = ""
    camp_flg = False
    provider_id = b4[site_ord][0]
    site_name = b4[site_ord][1]
    camp_flg = b4[site_ord][2]
    arr_idx = site_ord # LW(0)
    if site_ord > 0:
        '''
        if b4[site_ord][2] == False and site_ord < 14 :
            arr_idx = site_ord*4+1
        elif b4[site_ord][2] == True or b4[site_ord][2] == False and site_ord >= 14 :
            arr_idx = 26+((site_ord-6)*2)
        '''
        if site_ord == 1 : # LS
            arr_idx = 5
        if site_ord == 2 : # MD
            arr_idx = 9
        if site_ord == 3 : # LD
            arr_idx = 13
        if site_ord == 4 : # NP
            arr_idx = 17
        if site_ord == 5 : # PS
            arr_idx = 21
        if site_ord == 6 : # 강남P
            arr_idx = 26
        if site_ord == 7 : # 신촌P
            arr_idx = 28
        if site_ord == 8 : # 강남MD종
            arr_idx = 30
        if site_ord == 9 : # 부산P
            arr_idx = 32
        if site_ord == 10 : # 대구P
            arr_idx = 34
        if site_ord == 11 : # 강북P
            arr_idx = 36
        if site_ord == 12 : # 서초P
            arr_idx = 38
        if site_ord == 13 : # 광주P
            arr_idx = 40
        if site_ord == 14 : # MS
            arr_idx = 42
        if site_ord == 15 : # ME
            arr_idx = 46
    #print(site_ord)
    #print(arr_idx)
    #SITE CSV LOAD
    driver.add_cookie({'name' : 'selected_user_content_provider_id','value' : provider_id})
    driver.get("http://kr.kollus.com/media/analytics/traffic.csv?from_date="+s_dt+"&to_date="+e_dt) 
    if camp_flg == False:        
        driver.get("http://kr.kollus.com/media/analytics/transfer.csv?from_date="+s_dt+"&to_date="+e_dt) 
        driver.get("http://kr.kollus.com/media/analytics/visitor.csv?from_date="+s_dt+"&to_date="+e_dt) 

    driver.get("http://kr.kollus.com/media/analytics/stats/storage")

    dn_btn = driver.find_element_by_xpath("//button[@class='btn btn-primary btn-download btn__download']")
    dn_btn2 = driver.find_element_by_xpath("//button[@class='btn dropdown-toggle']")

    start_dt = driver.find_element_by_id("form-from-date")
    end_dt = driver.find_element_by_id("form-to-date")

    start_dt.clear()
    start_dt.send_keys(s_dt)
    end_dt.clear()
    end_dt.send_keys(e_dt)


    dn_btn.click()
    dn_btn2.click()

    # download time wait
    #time.sleep(2)

    file1 = file_down_path+'\\'+site_name+'-traffic-'+s_dt+'-'+e_dt+'.csv'
    if camp_flg == False:        
        file2 = file_down_path+'\\'+site_name+'-transfer-'+s_dt+'-'+e_dt+'.csv'
        file3 = file_down_path+'\\visitors-'+s_dt+'-'+e_dt+'.csv'        
    
    file4 = file_down_path+'\\'+site_name+'-storage_'+s_dt.replace("-","")+'-'+e_dt.replace("-","")+'.csv'
    
    file1_dn_flg = 0
    file2_dn_flg = 0
    file3_dn_flg = 0
    file4_dn_flg = 0

    while file1_dn_flg < 1:
        if os.path.isfile(file1):
            file1_dn_flg = file1_dn_flg + 1
            break
        else:
            time.sleep(1)
    
    if file1_dn_flg > 0:
        with open(file1, 'rt', encoding='UTF8') as f : 
            reader = csv.DictReader(f)
            arrCnt = 0
            for line in reader:
                if arrCnt <= diff.days:
                    if site_ord == 0:
                        b5[arrCnt][arr_idx] = line['날짜']
                        b5[arrCnt][arr_idx+1] = line['트래픽 사용량(bps)']
                    else:
                        b5[arrCnt][arr_idx] = line['트래픽 사용량(bps)']
                    arrCnt += 1
            f.close()
    if camp_flg == False:
        while file2_dn_flg < 1:
            if os.path.isfile(file2):
                file2_dn_flg = file2_dn_flg + 1
                break
            else:
                time.sleep(1)
        if file2_dn_flg > 0:
            with open(file2, 'rt', encoding='UTF8') as f :     
                reader = csv.DictReader(f)    
                arrCnt = 0
                for line in reader:        
                    if arrCnt <= diff.days:
                        if site_ord == 0:
                            b5[arrCnt][arr_idx+2] = line['전송량(GB)']
                        else:
                            b5[arrCnt][arr_idx+1] = line['전송량(GB)']
                        arrCnt += 1
                f.close()
        while file3_dn_flg < 1:
            if os.path.isfile(file3):
                file3_dn_flg = file3_dn_flg + 1
                break
            else:
                time.sleep(1)
        if file3_dn_flg > 0:
            with open(file3, 'rt', encoding='UTF8') as f :     
                reader = csv.DictReader(f)    
                arrCnt = 0
                for line in reader:
                    if site_ord == 0:
                        b5[arrCnt][arr_idx+3] = line['방문자']
                    else:
                        b5[arrCnt][arr_idx+2] = line['방문자']
                    arrCnt += 1
                f.close()
    while file4_dn_flg < 1:
        if os.path.isfile(file4):
            file4_dn_flg = file4_dn_flg + 1
            break
        else:
            time.sleep(1)
    if file4_dn_flg > 0:
        with open(file4, 'rt', encoding='UTF8') as f :     
            reader = csv.DictReader(f)    
            arrCnt = 0
            for line in reader:
                if arrCnt <= diff.days:
                    if site_ord == 0:
                        b5[arrCnt][arr_idx+4] = line['Total Size(Byte)']                
                    else:
                        if camp_flg == False:
                            b5[arrCnt][arr_idx+3] = line['Total Size(Byte)']
                        else:
                            b5[arrCnt][arr_idx+1] = line['Total Size(Byte)']                    
                arrCnt += 1
            f.close()

    if os.path.isfile(file1):
        os.remove(file1)
    if camp_flg == False:        
        if os.path.isfile(file2):
            os.remove(file2)
        if os.path.isfile(file3):
            os.remove(file3)

    if os.path.isfile(file4):
        os.remove(file4)


# 데이터 조회 S       
fnGetKollusData(0)
fnGetKollusData(1)
fnGetKollusData(2)
fnGetKollusData(3)
fnGetKollusData(4)
fnGetKollusData(5)
fnGetKollusData(6)
fnGetKollusData(7)
fnGetKollusData(8)
fnGetKollusData(9)
fnGetKollusData(10)
fnGetKollusData(11)
fnGetKollusData(12)
fnGetKollusData(13)
fnGetKollusData(14)
fnGetKollusData(15)
# 데이터 조회 E

# 데이터 출력
#print(b5)
df = pd.DataFrame(b5)
df.to_csv("output.csv",header=None, index=None)
print('crawl success!!')
driver.close()