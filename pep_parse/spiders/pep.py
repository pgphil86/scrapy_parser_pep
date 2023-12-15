import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    '''
    Spider for working with PEP documents.
    '''

    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        '''
        Working with links from PEP documents.
        '''

        pages = response.css('section[id=numerical-index]').css('a[href^="pep-"]')
        for link in pages:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        '''
        Working with a separate PEP page.
        '''

        page = response.css('section[id=pep-page-section]')
        title = response.css('h1.page-title::text').get()
        data = {
            'number': int(page.css('li::text')[2].get().replace('PEP', '')),
            'name': title.partition('- ')[2],
            'status': response.css('dt:contains("Status") + dd ::text').get(),
        }
        yield PepParseItem(data)
