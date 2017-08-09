#!/usr/bin/env python
# coding=utf-8

import scrapy


class LagouSPider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['https://www.lagou.com']
    start_urls = [
        "http://www.lagou.com/jobs/list_Python"
    ]

    def parse(self, response):
        filename = response.url.split('.')[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
