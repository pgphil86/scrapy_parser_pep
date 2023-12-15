import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """
    Spider for working with PEP documents.
    """
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """
        Working with links from PEP documents.
        """
        yield from response.follow_all(
            css='section[id=numerical-index] a[href^="pep-"]',
            callback=self.parse_pep
        )

    def parse_pep(self, response):
        """
        Working with a separate PEP page.
        """
        data = {
            'number': int(response.css
                          ('section[id=pep-page-section] li::text')
                          [2].get().replace('PEP', '').strip()),
            'name': response.css('h1.page-title::text'
                                 ).get().partition('- ')[2],
            'status': response.css('dt:contains("Status") + dd ::text').get(),
        }
        yield PepParseItem(data)
