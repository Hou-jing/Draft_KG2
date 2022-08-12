
import os
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from multiprocessing.dummy import Pool as ThreadPool
from filepro import PassGJB, findPath, Writecsv


# 一直等待某元素可见，默认超时10秒
def is_visible(driver, locator, timeout=30):
    try:
        ui.WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

def Get_singlepdf(fpath):  # 识别单个PDF的内容
    # 无头浏览器
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    #指定下载路径
    out_path = r'E:\python project\pythonProject_draftKG\标准文件\转换文件'  # 是你想指定的路径
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(
        executable_path='C:\\Program Files\\Google\Chrome\\Application\\104.0.5112.79\\chromedriver',
        chrome_options=options)
    # driver = webdriver.Chrome(
    #     executable_path='C:\\Program Files\\Google\Chrome\\Application\\104.0.5112.79\\chromedriver')
    url = 'https://www.camscanner.com/pdftoword'
    driver.get(url)
    # fpath='E:\\python project\\pythonProject6.27\\标准PDF转化\\扫描件图片\\GBT 28874-2012 空间科学实验数据产品分级规范\\images_3.png'
    driver.find_element_by_xpath("//input[@type='file']").send_keys(fpath)
    time.sleep(5)
    if is_visible(driver, '//*[@id="app"]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div'):
        driver.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div').click()  # 触发复制
        time.sleep(5)
        print('{}转换成功'.format(fpath.split('\\')[-1]))

#识别一个dir的PDF文件
if __name__=='__main__':
    path='E:\\python project\\pythonProject_draftKG\\标准文件\\转换文件'
    if not os.path.exists(path):
        os.mkdir(path)
    pool = ThreadPool(2)
    dir = 'E:\\python project\\pythonProject_draftKG\\标准文件'
    flist = findPath().getAllPaths(dir)
    print(flist)


    flist = findPath().getAllPaths(dir)
    newflist = Writecsv(flist)
    print('全部文件总量为{}'.format(len(newflist)))
    trans_dir = 'E:\\python project\\pythonProject_draftKG\\标准文件\\转换文件'
    trans_file_list = findPath().getAllPaths(trans_dir)  # 转换的文件列表

    no_trans_file = list(set(newflist) - set(trans_file_list))
    results = pool.map(Get_singlepdf, no_trans_file)



