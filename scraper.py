import grequests
import time
from bs4 import BeautifulSoup

start_time = time.time()

links = [f"https://www.bbc.com/zhongwen/trad/topics/cq8nqywy37yt/page/{page}" for page in range(1,4)]
print(links)
#建立GREQUEST 的處理池平行發送請求
reqs = (grequests.get(link) for link in links)
responses = grequests.imap(reqs, grequests.Pool(3))#有三個網頁所以設定3
for index, response in enumerate(responses):
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
    sub_links =[url.get('href') for url in urls]
    sub_reqs = (grequests.get(sub_link) for sub_link in sub_links)
    sub_responses = grequests.imap(sub_reqs , grequests.Pool(10))
    tag_list = []
    for sub_response in sub_responses:
        sub_soup = BeautifulSoup(sub_response.text,'lxml')
        tags = sub_soup.find_all('li',{'class','bbc-1msyfg1 e2o6ii40'})
        for tag in tags:
            tag_list.append(tag.getText())


    print(f"第{index+1}頁")
    print(title_list)
    print(tag_list)


end_time = time.time()
print(f"花費{end_time-start_time}秒")