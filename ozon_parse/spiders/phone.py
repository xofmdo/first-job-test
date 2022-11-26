import scrapy

from ozon_parse.items import OzonPhoneItem


class PhoneSpider(scrapy.Spider):
    name = "phones"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.ozon.ru/category/smartfony-15502/?sorting=rating",
            callback=self.parse_list,
        )
        self.phone_links = []

    def parse_list(self, response):
        for link in response.css("a.tile-hover-target.k8n::attr(href)"):
            self.phone_links.append(link.get())

        next_page_number = int(response.css("a.ama.aam0::text").get()) + 1

        if len(self.phone_links) < 100:
            new_link = f"https://www.ozon.ru/category/smartfony-15502/?page=" \
                       f"{next_page_number}&sorting=rating "
            yield scrapy.Request(
                url=new_link,
                callback=self.parse_list,
            )
        else:
            for link in self.phone_links[:100]:
                link = link.split("?")[0]
                next_page = 'https://www.ozon.ru'+link
                yield scrapy.Request(
                    url=next_page,
                    callback=self.parse_phone,
                    dont_filter=True,
                )

    def parse_phone(self, response):
        name = response.xpath("//h1[@class='vn0']/text()").get()
        os = response.xpath(
            "//dl[dt[span[contains(text(), 'Версия')]]]/dd//text()"
        ).get()
        print(self.phone_links)
        if not os:
            os = "Нет информации об OS"
        yield OzonPhoneItem(name=name, os=os)
