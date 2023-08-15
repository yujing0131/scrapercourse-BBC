import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.bbc.com/zhongwen/trad/topics/cq8nqywy37yt")

soup = BeautifulSoup(response.text,'lxml')

titles = soup.find_all(
    'a',{'class':'focusIndicatorDisplayBlock bbc-uk8dsi e1d658bg0'})
#print(titles)
title_list = []
for title in titles:
    title_list.append(title.getText())

#print(title_list)


##搜尋網頁子網址，並將網頁下標籤整合到一個串列中
urls = soup.find_all(
    'a',{'class':'focusIndicatorDisplayBlock bbc-uk8dsi e1d658bg0'})
tag_list = []
for url in urls:
    sub_response = requests.get(url.get('href'))
    sub_soup = BeautifulSoup(sub_response.text,'lxml')
    tags = sub_soup.find_all('li',{'class','bbc-1msyfg1 e2o6ii40'})
    for tag in tags:
        #print(tag.getText())
        tag_list.append(tag.getText())
    #print(sub_soup)
    #url_list.append(url.get('href'))


print(tag_list)