import requests
from bs4 import BeautifulSoup
#設定發送請求的http標頭
header = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

##設定例外機制
try:
    response =requests.get("https://www.bbc.com/zhongwen/trad/topics/cq8nqywy37yt"
                        ,headers=header
                        ,timeout=5)#設定超過5秒就停止發送請求

    if response.status_code==200:
        soup = BeautifulSoup(response.text,'lxml')
        titles = soup.find_all('a',{'class':'focusIndicatorDisplayBlock bbc-uk8dsi e1d658bg0'})
        #確定元素是否存在，若不存在則列印出錯誤訊息
        if titles!=[]:
            result = [title.getText() for title in titles]
            print(result)
        else:
            print('元素不存在')
    else:
        print('狀態碼非200!')
#若發生例外的錯誤則列印錯誤訊息
except Exception as e:
    print(str(e))