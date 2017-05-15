#!/usr/bin/env python
# coding=utf-8

from lxml import etree
import requests
from http import cookiejar
from PIL import Image
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windos NT 10.0; WOW64;rv:53.0)Gecko/20100101 Firefox/53.0',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.zhihu.com'
}


class MyClient(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers = headers
        self.cookies = cookiejar.LWPCookieJar(filename='cookies')
        try:
            self.cookies.load()
        except OSError:
            self._login()

    def _login(self):
        #username = input('请输入账号： ')
        #password = input('请输入密码： ')
        username = os.environ['my_username']
        password = os.environ['my_password']
        _xsrf = self._get_xsrf()
        captcha = self._get_captcha()
        postData = {
            'username': username,
            'password': password,
            '_xsrf': _xsrf,
            'captcha': captcha,
            'remember_me': 'true'
        }
        if '@' in username:
            login_url = 'https://www.zhihu.com/login/email'
        elif username.isdigit():
            login_url = 'https://www.zhihu.com/login/phone_num'
        else:
            print('账号错误')
        res = self.post(login_url, data=postData)
        if res.json()['r'] == 0:
            print('登陆成功')
            self.cookies.save()
        else:
            print('登陆错误')
            print('错误信息： ', res.json()['msg'])
            q = input('是否重新登陆:y/n')
            if q == 'y':
                self._login()

    def _get_xsrf(self):
        html = self.get_xpath('https://www.zhihu.com')
        xsrf = html.xpath('//input[contains(@name, "_xsrf")]/@value')
        return xsrf[0]

    def _get_captcha(self):
        captcha_url = 'https://www.zhihu.com/captcha.gif'
        with open('captcha.gif', 'wb') as f:
            f.write(self.get(captcha_url).content)
        im = Image.open('captcha.gif')
        im.show()
        im.close()
        captcha = input('请输入验证码：')
        return captcha

    def get_xpath(self, url):
        html = self.get(url)
        try:
            detail = etree.HTML(html.text.encode(html.encoding).decode('utf-8'))
            return detail
        except TypeError:
            print('url: %s  网页是空的或者IP被封' % url)
            return None
