import requests
from bs4 import BeautifulSoup
import time
import concurrent.futures

def scrape(links):
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text,'lxml')
        titles = soup.find_all(
            'h2',{'class':'bbc-10m3zrw e47bds20'})

        title_list = []
        for title in titles:
            title_list.append(title.getText())


        urls = soup.find_all(
            'a',{'class':'focusIndicatorDisplayBlock bbc-uk8dsi e1d658bg0'})
        tag_list = []
        for url in urls:
            #print(url.get('href'))
            sub_response = requests.get(url.get('href'))
            sub_soup = BeautifulSoup(sub_response.text,'lxml')
            tags = sub_soup.find_all('li',{'class','bbc-1msyfg1 e2o6ii40'})
            for tag in tags:
                #print(tag.getText())
                tag_list.append(tag.getText())

    
        print(title_list)
        print(tag_list)


start_time = time.time()
##必須建立網址清單
links = [f'https://www.bbc.com/zhongwen/trad/topics/c83plve5vmjt?page={page}' for page in range(1,4)]
print(links)
#同時建立和啟用多個執行緒。設定有10個執行緒
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(scrape,links)

end_time = time.time()
print(f"花費{end_time-start_time}秒")