#!/usr/bin/env python
# coding=utf-8

import requests
import re
from lxml import etree


class spider():
    def __init__(self):
        print('Began to crawl...')

    def get_html(self,url):
        html = requests.get(url)
        return html.text

    def change_url(self,url):
        now_page=int(re.search('\?s=(\d+)', url, re.S).group(1))
        page_group = []
        for i in range(5):
            link = re.sub('\?s=\d+', '?s=%s' % (now_page+i), url, re.S)
            page_group.append(link)
        return page_group

    def get_content(self, html):
        html=etree.HTML(html)
        contents=html.xpath('//div[contains(@class,"content")]/span/text()')
        return contents


if __name__ == '__main__':
    qiubai = spider()
    print('look joke...')
    url='https://www.qiushibaike.com/8hr/page/2/?s=4971313'
    url_list=qiubai.change_url(url)
    for url in url_list:
        print('Are deadling with: ' + url)
        html=qiubai.get_html(url)
        contents=qiubai.get_content(html)
        for each in contents:
            print(each)
        
