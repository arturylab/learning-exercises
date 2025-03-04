import scrapy

class FinanceSpider(scrapy.Spider):
    name = 'finance'
    symbols = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA']
    
    def start_requests(self):
        for symbol in self.symbols:
            url = f'https://finance.yahoo.com/quote/{symbol}'
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        stock_name = response.css('h1.yf-xxbei9::text').get()
        stock_price = response.css('.base.yf-ipw1h0::text').get()

        yield {
            'stock_name': stock_name,
            'stock_price': stock_price,
        }
