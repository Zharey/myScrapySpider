# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from autoComplaints.items import AutocomplaintsItem
class CarspiderSpider(scrapy.Spider):
    name = 'carSpider'

    def start_requests(self):
        start_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-5835.shtml'
        yield SplashRequest(start_url, self.parse, args={'wait': '0.5', 'images': '0'})

    def parse(self, response):
        cars = response.css('div.tslb_b tr')
        item = AutocomplaintsItem()
        for car in cars:
            item['tspp'] = car.css('td:nth-child(2)::text').extract()
            item['tscx'] = car.css('td:nth-child(3)::text').extract()
            item['tscxing'] = car.css('td:nth-child(4)::text').extract()
            item['tsjs'] = car.css('td.tsjs a::text').extract()
            item['tsbw'] = str(car.css('td.tsgztj span.bw a::text').extract())
            item['tswt'] = str(car.css('td.tsgztj span.wt a::text').extract())
            item['tsfw'] = str(car.css('td.tsgztj span.fwwt a::text').extract())
            item['fwwt'] = str(car.css('td.tsgztj span.fw a::text').extract())
            item['tssj'] = car.css('td:nth-child(7)::text').extract()
            if item['tspp'] is not None and (str(item['tssj']) > '2014-12-31'):
                yield item
        next_page = response.css('div.p_page a:contains("下一页")::attr(href)').extract_first()
        if next_page is not None:
            next_url = response.urljoin(next_page)
            yield SplashRequest(next_url, self.parse, args={'wait': '0.5', 'images': '0'})

