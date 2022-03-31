import scrapy


class BestSellerSpider(scrapy.Spider):
    name = 'best_seller'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        rows = response.xpath(
            '//div[@class="col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center product-list-item"]')
        for item in rows:
            product_url = item.xpath(
                './/div[@class="product-img-outer"]/a/@href').get()

            # Get image link
            clas_check_img = item.xpath(
                './/div[@class="product-img-outer"]/a/@class').getall()
            for clas in clas_check_img:
                if "none" not in clas:
                    images_links = item.xpath(
                        f'.//a[@class="{clas}"]/img[1]/@data-src').get()

            product_name = item.xpath(
                'normalize-space(.//div[@class="p-title"]/a[1]/text())').get()
            price = item.xpath(
                './/div[@class="p-price"]/div[1]/span[1]/text()').get()

            yield{
                "Product URL": product_url,
                "Product Name": product_name,
                "Product Price": price,
                "Image Link": images_links
            }

            # pagination
            next_page = response.xpath('//a[@rel="next"]/@href').get()
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)
