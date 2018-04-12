import scrapy
from scrapy.http import Request
from job.items import JobItem

#数据类招聘信息
class  JobSplider(scrapy.spiders.Spider):
    name="job"
    #position ETL，数据仓储，数据开发，数据挖掘，数据分析，数据架构
    positions=[100506,100507,100508,100509,100511,100512]
    #city 北京，上海，广州，深圳，杭州，苏州
    cities=[101010100,101020100,101280100,101280600,101210100,101190400]
    start_urls=[]
    for p in positions:
        for c in cities:
            url="https://www.zhipin.com/job_detail/?query=&scity="+str(c)+"&industry=&position="+str(p)
            start_urls.append(url)
    # start_urls = "https://www.zhipin.com/job_detail/?query=&scity=101280600&industry=&position=100508"#深圳


    def parse(self,response):
        for result in response.xpath('//*[@id="main"]/div/div[2]/ul/li'):
            jobName=result.xpath('div/div[1]/h3/a/div[1]/text()').extract()[0]
            salary=result.xpath('div/div[1]/h3/a/span/text()').extract()[0]
            address_during_education = result.xpath('div/div[1]/p/text()').extract()[0]
            company=result.xpath('div/div[2]/div/h3/a/text()').extract()[0]
            url = result.xpath('div/div[1]/h3/a/@href').extract()[0]

            item = JobItem()
            item['jobName']=jobName
            item['salary'] = salary
            item['info'] = address_during_education
            item['company'] = company

            #检索详细信息
            # yield Request(url, callback=self.parse_item, meta={'item': item})

            #翻页
            next_page_url = response.xpath('//*[@id="main"]/div/div[2]/div[2]/a[5]/@href').extract()[0]
            if next_page_url != 'javascript:void(0)':
                yield scrapy.Request(next_page_url, callback=self.parse)

    #该死的BOSS封我IP
    def parse_item(self,response):
        item = response.meta['item']
        for result in response.xpath('//*[@id="main"]/div/div[2]/ul/li'):
            info = result.xpath("~")


