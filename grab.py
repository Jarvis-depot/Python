# UA: User-Agent (请求载体的身份标识)
# UA检测: 门户网站的服务器会检测对应请求的载体身份标识，如果检测到身份标识为某一款浏览器(说明是用户通过浏览器发起的)
# 说明该请求是一个正常的请求
# 如果请求不是经过浏览器发起的，那么认为不是一个正常的请求。那么服务器可能会拒绝该请求

# UA伪装： 让爬虫对应的请求载体身份标识，伪装成某一款浏览器
import requests

# UA伪装：将对应的User agent封装到字典中
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
url = 'https://sogou.com/web?'
# 1. 处理url携带的参数：封装到字典中
# 从输入参数获取
kw = input('Enter a word: ')
param = {
    'query': kw
}
# 2. 对指定的url发起的请求对应的url是携带参数的，并且请求过程中处理了参数
# UA伪装：此处用headers进行伪装
response = requests.get(url=url, params=param, headers=headers)
# 3. 获取响应数据
page_test = response.text
# 4. 对响应数据做持久化存储
fileName = kw + '.html'
with open(fileName, 'w', encoding='utf=8') as fp:
    fp.write(page_test)
print(fileName, 'Saving...')
