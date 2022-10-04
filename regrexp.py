import requests
import re
import os


def regexp_grab_jpg():
    if not os.path.exists('./pictures'):
        os.mkdir('./pictures')
    num = 0
    url = 'https://699pic.com/tupian/sheying.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    # 使用通用爬虫对url页面进行爬取
    page_text1 = requests.get(url=url, headers=headers).text
    # 使用聚焦爬虫将页面中所有的图片进行解析和截取
    ex1 = '<a href="\\S+tupian\\S+html"'
    # re.S: 单行匹配
    # re.M: 多行匹配
    img_path_list1 = re.findall(ex1, page_text1, re.S)
    print(img_path_list1)
    for path1 in img_path_list1:
        path1 = path1.split('"')[1]
        img_path = 'https:' + path1
        page_text2 = requests.get(url=img_path, headers=headers).text
        ex2 = 'data-original="(\\S+jpg)'
        img_path_list2 = re.findall(ex2, page_text2, re.S)
        for path2 in img_path_list2:
            path2 = 'https:' + path2
            img_name = str(num) + '.jpg'
            img_path = './pictures/' + img_name
            img_data = requests.get(url=path2, headers=headers).content
            num += 1
            with open(img_path, 'wb') as fp:
              fp.write(img_data)
              print(img_name, "下载成功！！！")
        exit(1)

regexp_grab_jpg()
