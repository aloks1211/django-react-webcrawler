import aiohttp
from lxml import html
from urllib.parse import urljoin, urlparse
from djangocrawler.logger import log


class UrlFinder(object):
    def __init__(self,seed_url,depth,loop):
        self.seed_url = seed_url
        self.depth = depth
        self.urls_traversed = set()
        timeout = aiohttp.ClientTimeout(total=10*60)
        self.client_session = aiohttp.ClientSession(timeout=timeout,loop=loop)
        self.domain_url ='{}://{}'.format(urlparse(self.seed_url).scheme, urlparse(self.seed_url).netloc)

    async def _get_html(self,url):
        """

        :param url:
        :return:
        """
        try:
            async with self.client_session.get(url, ssl =False) as response:
                html_text = await response.content.read()
                return html_text
        except Exception as e:
            log.exception (e.__str__())

    async def _get_all_urls(self,html_text):
        """

        :param html_text:
        :return:
        """
        urls_found =[]
        try:
            links = html.fromstring(html_text)
            for link in links.xpath('//a/@href'):
                final_url = urljoin(self.domain_url,link)
                if final_url not in self.urls_traversed and final_url.startswith(self.domain_url):
                    urls_found.append(final_url)
            return urls_found
        except Exception as e:
            log.exception(e.__str__())

    async def crawl_page_async(self,url):
        """

        :param url:
        :return:
        """
        final_urls = []
        html_text = await self._get_html(url)
        try:
            if html_text:
                final_urls = await self._get_all_urls(html_text)
                return url, sorted(final_urls)
            else:
                log.info ("no text found for the url: {0}".format(url))
        except Exception as e:
            log.exception(e.__str__())












