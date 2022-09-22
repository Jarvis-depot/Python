# requests: 基于网络请求的模块
# 作用：模拟浏览器发请求

# Steps:
#   1. 指定URL
#   2. 发起请求
#   3. 获取响应数据
#   4. 持久化存储

import requests
if __name__ == "__main__":
    # 1. 指定URL
    url = 'https://www.sogou.com'
    # 2. 发起请求 (get方法会返回一个响应对象)
    response = requests.get(url=url)
    # 3. 获取响应数据 (返回的是字符串形式的响应数据)
    page_text = response.text
    print("page text is:", page_text)
    # 4. 持久化存储
    with open('./sogou.html', 'w', encoding='utf-8') as fp:
      fp.write(page_text)
    print('Finished')