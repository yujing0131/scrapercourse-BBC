import requests
from bs4 import BeautifulSoup

header = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

try:
    response = requests.get('https://www.bbc.com/zhongwen/trad/topics/c83plve5vmjt',headers=header,timeout=10)
    if response.status_code==200:
        soup = BeautifulSoup(response.text, 'lxml')

        titles = soup.find_all('a', {'class': 'focusIndicatorDisplayBlock bbc-uk8dsi e1d658bg0'})
        if titles !=[]:
            result =[title.getText() for title in titles]
            print(result)
        else:
            print('元素不存在!')
    else:
        print('狀態碼非200')
except Exception as e:
    print(str(e))
        