import requests
from bs4 import BeautifulSoup


for page in range(1,4):
    response = requests.get("https://www.bbc.com/zhongwen/trad/topics/c83plve5vmjt/page/{page}")

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

    print(f"第{page}頁")
    print(title_list)
    print(tag_list)