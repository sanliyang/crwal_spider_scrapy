import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QySpider(CrawlSpider):
    name = 'qy'
    allowed_domains = ['qcc.com']
    start_urls = ['https://www.qcc.com/g_AH']

    rules = (
        Rule(LinkExtractor(allow=r'g_[A-Z]{2,}',
                           deny=r'g_[A-Z]{2,}_\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css='.pagination-md'), callback='parse_item',follow=True)
    )

    def parse_item(self, response):
        trs = response.css('.m_srchList tr')
        for tr in trs:
            item = {}
            item['cover'] = tr.xpath('./td[1]/img/@src').get()
            item['name'] = tr.xpath('./td[2]/a/text()').get()
            item['cp_name'] = tr.xpath('./td[2]/p[1]/a/text()').get()
            item['phone'] = tr.xpath('./td[2]/p[2]/span/text()').get()
            item['address'] = tr.xpath('./td[2]/p[3]/text()').get().replace('\n','').strip()
            yield item
