import requests
import json


# 由于KFC官网查询页面，输入查询省份后，网址没有变化。因此认为是一个阿贾克斯请求
def get_kfc_restaurants():
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx'
    word = input('Enter a city: ')
    size = input('How many results you wanna check? ')
    data = {
        'op': 'keyword',
        'cname': '',
        'pid': '',
        'keyword': word,
        'pageIndex': '1',
        'pageSize': size,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    # response = requests.get(url=url, data=data, headers=headers)
    response = requests.get(url=url, params=data, headers=headers)
    list_data = response.json()
    fp = open('./kfc.json', 'w', encoding='utf-8')
    json.dump(list_data, fp=fp, ensure_ascii=False)
    fp.close()


get_kfc_restaurants()
