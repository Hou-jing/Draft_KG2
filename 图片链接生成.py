import json
import os
import re
import time
import pyperclip
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 一直等待某元素可见，默认超时10秒
def is_visible(driver,locator, timeout=10):
    try:
        ui.WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

#上传一张图片
def Getsingurl(fpath):
    # fpath='E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件图片\\22-AIAA G-113-10-2013 Space Plug-and-Play Architecture guide System Capabilities.docx\\22-AIAA G-113-10-2013 Space Plug-and-Play Architecture guide System Capabilitiesimage3.png'
    url = 'https://sm.ms/'
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="smfile"]').send_keys(fpath)

    js="var q=document.documentElement.scrollTop=500"
    driver.execute_script(js)
    driver.find_element_by_xpath(
        '/html/body/div[1]/form[1]/div/div/div[4]/div[2]/a'
    ).click()
    time.sleep(1)
    try:
        if is_visible(driver,'/html/body/div[1]/form[1]/div/div/div[2]/div/div'):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            urlele=driver.find_element_by_xpath('//*[@id="imagedetail"]/fieldset/table/tbody/tr/td[2]/div[8]/div/div/input')
            imgurl=urlele.get_attribute('value')
            return imgurl
    except Exception as e:
        pass

def Getallurl():
    base_dir='E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件图片'
    file_dir=os.listdir(base_dir)
    filed={}
    for fdir in file_dir[:7]:
        fname=os.listdir(base_dir+'\\'+fdir)
        urls = []
        for name in fname:
            imgurl=Getsingurl(base_dir+'\\'+fdir+'\\'+name)
            urls.append(imgurl)
        filed[fdir]=urls
        print('{}转换完成'.format(fdir))

    return filed

#将抽取的文件内容保存，字典形式
def Savedic(fname,dir_dic):
    fp = open(fname, 'w+', encoding='utf_8')
    json.dump(dir_dic, fp=fp, ensure_ascii=False, indent=1)


if __name__=='__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(
        executable_path='C:\\Program Files\\Google\Chrome\\Application\\104.0.5112.81\\chromedriver',
        chrome_options=options
    )
    url = 'https://sm.ms/'
    driver.get(url)
    driver.find_element_by_xpath('/html/body/div[1]/form[1]/div/div[1]/span/a').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys('houj')
    driver.find_element_by_xpath('//*[@id="password"]').send_keys('hou18833283973')
    driver.find_element_by_xpath('//*[@id="submiButton"]').click()
    time.sleep(3)

    filed=Getallurl()
    resdir='E:\python project\pythonProject_draftKG\文件信息结构化\文件内容'
    Savedic(resdir+'\\'+'imgurl.json',filed)