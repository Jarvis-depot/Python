import requests
import re
import os

def regrexp_grab_jpg():
    if not os.path.exists('./pictures'):
        os.mkdir('./pictures')
    num = 0;
    url = 'https://baijiahao.baidu.com/s?id=1745570748714472228'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    # 使用通用爬虫对url页面进行爬取
    page_text = requests.get(url=url, headers=headers).text
    # 使用聚焦爬虫将页面中所有的图片进行解析和截取
    ex = '<div class="index-module_contentImg_JmmC0">.*?src="(.*?)"'
    # re.S: 单行匹配
    # re.M: 多行匹配
    img_src_list = re.findall(ex, page_text, re.S)
    print(img_src_list)
    for src in img_src_list:
        img_name = str(num) + '.jpg'
        num += 1
        img_data = requests.get(url=src, headers=headers).content
        img_path = './pictures/' + img_name
        with open(img_path, 'wb') as fp:
            fp.write(img_data)
            print(img_name, "下载成功！！！")



regrexp_grab_jpg()