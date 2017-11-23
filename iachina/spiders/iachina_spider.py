# -*- coding: utf-8 -*-
import scrapy
import os
from iachina.items import IachinaItem


class IachinaSpiderSpider(scrapy.Spider):
    name = "iachina_spider"
    allowed_domains = ["iachina.cn"]
    start_urls = (
        'http://old.iachina.cn/product.php?action=company&ttype=2',
    )

    headers = {
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'referer': "http://old.iachina.cn/product.php?action=company&ttype=2",
        'cookie': "PHPSESSID=201ed6740a7231fd0670a7a5be2af784; Hm_lvt_3ea51289017d00e5265ee3f2f37be0a8=1511334288; Hm_lpvt_3ea51289017d00e5265ee3f2f37be0a8=1511336092",
        'proxy-connection': "keep-alive",
        'cache-control': "no-cache",
    }

    def parse(self, response):
        companies=response.css('div.prolist ul li a::text').extract()
        company_url=response.css('div.prolist ul li a::attr(href)').extract()

        for i in range(len(companies)):
            company_name=companies[i]
            url=company_url[i]

            yield  scrapy.Request(response.urljoin(url),headers=self.headers,meta={'company_name':company_name},callback=self.parse_product_type)


        next_page=response.css('div.cutpage a::attr(href)').extract()

        if next_page is not None and len(next_page)>0 and next_page[-1]!='javascript:;':
            yield scrapy.Request(response.urljoin(next_page[-1]),headers=self.headers,callback=self.parse)


    def parse_product_type(self,response):

        product_types = response.css('div.prolist ul li a::text').extract()
        product_type_url = response.css('div.prolist ul li a::attr(href)').extract()

        for i in range(len(product_types)):
            company_name=response.meta['company_name']

            product_type = product_types[i]
            url = product_type_url[i]

            yield scrapy.Request(response.urljoin(url), headers=self.headers,meta={"company_name":company_name,"product_type":product_type}, callback=self.parse_product_name)

        next_page = response.css('div.cutpage a::attr(href)').extract()

        if next_page is not None and len(next_page)>0  and next_page[-1]!='javascript:;' :
            yield scrapy.Request(response.urljoin(next_page[-1]), headers=self.headers,meta={"company_name":company_name}, callback=self.parse_product_type)



    def parse_product_name(self,response):


        product_names = response.css('div.prolist ul li a::text').extract()
        product_name_url = response.css('div.prolist ul li a::attr(href)').extract()

        for i in range(len(product_names)):
            company_name=response.meta['company_name']
            product_type=response.meta['product_type']
            product_name = product_names[i]
            url = product_name_url[i]

            yield scrapy.Request(response.urljoin(url), headers=self.headers,meta={"company_name":company_name,"product_type":product_type,"product_name":product_name}, callback=self.parse_clause_name)

        next_page = response.css('div.cutpage a::attr(href)').extract()

        if next_page is not None and len(next_page)>0 and next_page[-1] != 'javascript:;'  :
            yield scrapy.Request(response.urljoin(next_page[-1]), headers=self.headers,meta={"company_name":company_name,"product_type":product_type}, callback=self.parse_product_name)



    def parse_clause_name(self,response):
        clause_names = response.css('div.prolist tr td a::text').extract()
        clauses_urls = response.css('div.prolist tr td a::attr(href)').extract()

        for i in range(len(clause_names)):

            company_name=response.meta['company_name']
            product_name=response.meta['product_name']
            product_type=response.meta['product_type']

            clause_name = clause_names[i]
            url = clauses_urls[i]

            yield scrapy.Request(response.urljoin(url), headers=self.headers,meta={"company_name":company_name,"product_type":product_type,"product_name":product_name,"clause_name":clause_name},callback=self.parse_content)

        next_page = response.css('div.cutpage a::attr(href)').extract()

        if next_page is not None and len(next_page)>0 and next_page[-1] != 'javascript:;':
            yield scrapy.Request(response.urljoin(next_page[-1]), headers=self.headers,meta={"company_name":company_name,"product_type":product_type,"product_name":product_name}, callback=self.parse_clause_name)



    def parse_content(self,response):

        content=response.body

        content=content.decode('gb2312')
        item=IachinaItem()

        item['company_name']=response.meta['company_name']
        item['product_name']=response.meta['product_name']
        item['product_type']=response.meta['product_type']
        item['clause_name']=response.meta['clause_name']
        item['clause_url']=response.urljoin(response.url)
        item['content']=content
        filedir=('./data/{0}/{1}/{2}/{3}/'.format(item['company_name'],item['product_type'],item['product_name'],item['clause_name']))
        print(filedir)
        if not os.path.exists(filedir):
            os.makedirs(filedir)

        filename=filedir + item['clause_name'] + '.docx'
        print(filename)
        html = open(filename, 'w', encoding='gbk')
        html.write('''%s'''%content)
        html.close()

        yield item









