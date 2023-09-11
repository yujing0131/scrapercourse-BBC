# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 19:20:00 2023

@author: zifuera
"""
import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import os

# ------ 生成獨立檔名Function ------
def generate_unique_filename(filename):
    counter = 1
    base_name, ext = os.path.splitext(filename)
    while os.path.exists(filename):
        filename = f"{base_name}_{counter}{ext}"
        counter += 1
    return filename

# ------ Check the current directory ------
current_directory = os.getcwd()
print("Current working directory:", current_directory)

# ------ 透過Browser Driver 開啟 Chrome ------
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# driver = webdriver.Chrome()

# ------ 設定要前往的網址 ------
url = 'https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx'
driver.get(url)

# ------ 整理要輸入的值 ------
# strYear = '110'
# strMon = '1'
# strDay = '1'
# endYear = '111'
# endMon = '12'
# endDay = '31'

# judCourt = '臺灣臺中地方法院'
judCourt = '最高法院'
judYear = '112'
judCase = '台上'
judNo = '1'
judNoEnd = '10'

# ------ 等待頁面加載完畢 ------
wait = WebDriverWait(driver, 10)

# ------ Select the <select> element by its ID ------
select_element = Select(driver.find_element(By.ID, "jud_court"))

# ------ Select by visible text ------
select_element.select_by_visible_text(judCourt)

# ------ 因為checkbox id都一樣 ------
# ------ 1. 所以先找到所有label元素 ------
labels = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//label")))

# ------ 2. 遍歷label元素，查找的checkbox value是自己想要的值便點擊 ------
for label in labels:
    checkbox = label.find_element(By.XPATH, ".//input[@type='checkbox']")
    if checkbox.get_attribute("value") == 'M':
        checkbox.click()
        break

# ------ 填入要輸入的條件參數值 ------
driver.find_element(By.ID, "jud_year").send_keys(judYear)
driver.find_element(By.ID, "jud_case").send_keys(judCase)
driver.find_element(By.ID, "jud_no").send_keys(judNo)
driver.find_element(By.ID, "jud_no_end").send_keys(judNoEnd)
    
# ------ Locate and click the submit button ------
submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btnQry")))
submit_button.click()

# ------ 等待頁面加載完畢 ------
wait = WebDriverWait(driver, 10)

# ------ 指定要保存到的 pdf 文件名 ------
#csv_file = f"D:/外網統計園地/{judCourt}{judYear}{judCase}{judNo}-{judNoEnd}.csv"
pdf_file = f"D:/判決書PDF檔案/{judCourt}{judYear}{judCase}{judNo}.pdf"

# ------ 產生一個唯一的檔名，如果檔名已存在 ------
csv_file = generate_unique_filename(pdf_file)

# ------ define a title of a csv ------
data = [
        # ['序號', '裁判字號(內容大小)', '裁判日期', '裁判案由']
]

try:
    # ------ Switch to the iframe containing the table ------
    iframe = wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframe-data")))
    
    # ------ Wait for the table to be present ------
    table = wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
    
    # ------ Find all the <td> elements inside the table ------
    cells = table.find_elements(By.XPATH, ".//td")

    # ------ Loop through the <td> elements and print their text content ------
    i = 0
    array = []
    for cell in cells:
        i += 1
        if i%5 != 0:
            #value = cell.text
            #print(value)
            #array.append(value)
            #點擊搜尋到的判決
            link = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"hlTitle\"]"))).get_attribute('href')
            Title = wait.until(EC.presence_of_element_located((By.ID, "hlTitle")))
            Title.click()
            content = BeautifulSoup(requests.get(link).text, "html.parser")
            print(content.prettify())  #輸出排版後的HTML內容
            

            
            ##點擊轉乘pdf檔案按鈕
            # ConvertPDF_Button = wait.until(EC.element_to_be_clickable((By.ID, "hlExportPDF")))
            # ConvertPDF_Button.click()
            
        if i%5 == 0:
            data.append(array)
            array = []

except (TimeoutException, NoSuchElementException) as e:
    print("Table not found:", e)

    
# ------ 使用 'w' 模式打開文件，並創建 CSV writer 對象 ------
# with open(csv_file, 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)

#     # ------ 使用 writerow 寫入表頭 ------
#     writer.writerow(data[0])

#     # ------ 使用 writerows 寫入數據行 ------
#     writer.writerows(data[1:])

# print(f'Data saved to {csv_file} successfully.')
# driver.quit()