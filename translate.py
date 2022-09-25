# 1. 进入百度翻译的页面，同时开启检查
# 2. 将下方的All换成XHR，在翻译输入框中键入：dog。此时下方出现多个Name，一个一个点击
# 3. Payload: 可以看到每个sug(阿贾克斯请求)的内容，找到dog
# 4. Headers: 此处可以看到，Content-Type是application/json，说明返回的是json串
# 5. Response: 此处便是上述提到的json串

import requests
import json


def translate():
    # 1. 指定url
    post_url = 'https://fanyi.baidu.com/sug'
    # 2. 进行UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    # 3. post请求参数处理 (同get请求一致)
    word = input('enter a word: ')
    data = {
        'kw': word
    }
    # 4. 请求发送
    response = requests.post(url=post_url, data=data, headers=headers)
    # 5. 获取响应数据，当前的响应数据类型是json (json方法返回的是json对象，比如字典)
    dic_obj = response.json()
    # 6. 进行持久化存储
    fp = open('./translate.json', 'w', encoding='utf-8')
    json.dump(dic_obj, fp=fp, ensure_ascii=False)
    fp.close()
    print('Translate Done...')


translate()
