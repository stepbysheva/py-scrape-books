import scrapy
from scrapy.http import Response


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    @staticmethod
    def parse_single_page(response):
        title = response.css(".product_main h1::text").get()
        price = response.css(".product_main p::text").get().replace("$", "")
        description = response.css(".product_page>p::text").get()
        in_stock = int(response.css(".product_page>table tr")[5].css("td::text").get().split("(")[1].replace("available)", ""))
        rating = response.css(".star-rating::attr(class)").get().split(" ")[1]
        category = response.css(".breadcrumb li")[2].css("a::text").get()
        upc = response.css(".product_page>table tr")[0].css("td::text").get()
        yield {"title": title,
               "price": price,
               "in_stock": in_stock,
               "rating": rating,
               "category": category,
               "description": description,
               "upc": upc}

    def parse(self, response: Response, **kwargs) -> None:
        products = response.css(".product_pod")
        for product in products:
            yield response.follow(url=product.css("a::attr(href)").get(), callback=self.parse_single_page)

        if response.css(".pager>.next") is not None:
            yield response.follow(url=response.css(".pager>.next>a::attr(href)").get(), callback=self.parse)
