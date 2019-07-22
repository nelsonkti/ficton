# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Fiction.items import FictionItem
import re

class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['quanshuwang.com']
    start_urls = [
        # 'http://www.quanshuwang.com/list/1_2.html',
        # 'http://www.quanshuwang.com/list/1_3.html',
        # 'http://www.quanshuwang.com/list/1_4.html',
        # 'http://www.quanshuwang.com/list/1_5.html',
        # 'http://www.quanshuwang.com/list/1_6.html',
        # 'http://www.quanshuwang.com/list/1_7.html',
        # 'http://www.quanshuwang.com/list/1_8.html',
        # 'http://www.quanshuwang.com/list/1_9.html',
        # 'http://www.quanshuwang.com/list/1_10.html',
        # 'http://www.quanshuwang.com/book/115/115724',
        'http://www.quanshuwang.com/book/165/165601',
    ]

    def parse(self, response):
        ## 获取全部章节的小说
        chapter_urls = response.xpath('//div[@class="clearfix dirconone"]/li/a/@href').extract()
        i = 0
        for chapter_url in chapter_urls:
            i += 1
            yield Request(chapter_url, meta={'chapter_num': i}, callback=self.parse_content)


    #
    def parse_content(self, response):
        # 小说名字
        name = response.xpath('//div[@class="main-index"]/a[@class="article_title"]/text()').extract_first()

        result = response.text
        # 小说章节名字
        chapter_name = response.xpath('//strong[@class="l jieqi_title"]/text()').extract_first()
        # 小说章节内容
        chapter_content_reg = r'style5\(\);</script>(.*?)<script type="text/javascript">'

        chapter_content_2 = re.findall(chapter_content_reg, result, re.S)[0]
        chapter_content = ''.join(chapter_content_2)


        # chapter_content_1 = chapter_content_2.replace('    ', '')
        # chapter_content = chapter_content_1.replace('<br />', '')

        item = FictionItem()
        item['name'] = name
        item['chapter_name'] = chapter_name
        item['chapter_content'] = chapter_content
        item['chapter_num'] = response.meta['chapter_num']
        yield item



    # def parse(self, response):
    #     ## 小说列表
    #     book_urls = response.xpath('//li/a[@class="l mr10"]/@href').extract()
    #     for book_url in book_urls:
    #         yield Request(book_url, callback=self.parse_read)
    #
    # ## 循环每一本小说
    # def parse_read(self, response):
    #     read_url = response.xpath('//a[@class="reader"]/@href').extract()[0]
    #
    #     yield Request(read_url, callback=self.parse_chapter)
    # #
    # def parse_chapter(self, response):
    #     ## 获取全部章节的小说
    #     chapter_urls = response.xpath('//div[@class="clearfix dirconone"]/li/a/@href').extract()
    #
    #     for chapter_url in chapter_urls:
    #         yield Request(chapter_url, callback=self.parse_content)
    # #
    # def parse_content(self, response):
    #     # 小说名字
    #     name = response.xpath('//div[@class="main-index"]/a[@class="article_title"]/text()').extract_first()
    #     print('============================奥术大师多===========================')
    #     print(name)
    #     result = response.text
    #     # 小说章节名字
    #     chapter_name = response.xpath('//strong[@class="l jieqi_title"]/text()').extract_first()
    #     # 小说章节内容
    #     chapter_content_reg = r'style5\(\);</script>(.*?)<script type="text/javascript">'
    #     chapter_content_2 = re.findall(chapter_content_reg, result, re.S)[0]
    #     chapter_content_1 = chapter_content_2.replace('    ', '')
    #     chapter_content = chapter_content_1.replace('<br />', '')
    #
    #     item = FictionItem()
    #     item['name'] = name
    #     item['chapter_name'] = chapter_name
    #     item['chapter_content'] = chapter_content
    #     yield item

