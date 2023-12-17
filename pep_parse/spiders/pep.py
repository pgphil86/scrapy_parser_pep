import re
import scrapy

from pep_parse.items import PepParseItem
from pep_parse.constants import PEP_DOMAIN, PEP_REGULAR


class PepSpider(scrapy.Spider):
    """
    Spider for working with PEP documents.
    """
    name = 'pep'
    allowed_domains = [PEP_DOMAIN]
    start_urls = [f'https://{PEP_DOMAIN}/']

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
        title = re.search(PEP_REGULAR, response.css('h1.page-title::text').get())
        data = {
            'number': title.group('number'),
            'name': title.group('name'),
            'status': response.css('dt:contains("Status") + dd ::text').get()
        }
        yield PepParseItem(data)
