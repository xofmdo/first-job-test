import scrapy


class OzonPhoneItem(scrapy.Item):
    name = scrapy.Field()
    os = scrapy.Field()
