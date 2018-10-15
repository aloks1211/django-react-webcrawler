from webcrawler.crawler.urlfinder  import UrlFinder
from djangocrawler.queueserver import QueueServer
from lxml import html
import asyncio
from djangocrawler.logger import log


class ImageFinder(UrlFinder):
    def __init__(self,seed_url,depth,loop):
        super().__init__(seed_url, depth,loop)
        self.redis = QueueServer()

    async def get_images(self,urls=None):
        """

        :param urls:
        :return:
        """
        final_image_links = {}

        if urls:
            for url in urls:
                html_text = await self._get_html(url[1])
                if html_text:
                    doc_obj = html.fromstring(html_text)
                    # log.info ("no of images in url {0}:{1}".format(url,len(doc_obj.xpath('//img'))))
                    for image in doc_obj.cssselect('img'):

                        image_links = image.get('src')
                        if url[1] in final_image_links:
                            final_image_links[url[1]]["urls"].append(image_links)
                        else:
                            final_image_links[url[1]] = {}
                            final_image_links[url[1]]["depth"]= url[0]
                            final_image_links[url[1]]["urls"] = []
                            final_image_links[url[1]]["urls"].append(image_links)
                #self.redis.publish(final_image_links[url[1]])
        await self.client_session.close()
        return final_image_links

    async def extract_urls_recursive(self, to_fetch):
        """

        :param to_fetch:
        :return:
        """
        futures = list()
        final_urls_list = list()

        for url in to_fetch:
            if url in self.urls_traversed:
                continue
            self.urls_traversed.add(url)
            futures.append(self.crawl_page_async(url))
        for future in asyncio.as_completed(futures):
            try:
                final_urls_list.append((await future))
            except Exception as e:
                log.exception (e.__str__())
        return final_urls_list

    async def start_crawling(self):
        """

        :return:
        """
        urls_to_crawl = list()
        urls_to_crawl.append(self.seed_url)
        results = list()
        for depth in range(self.depth + 1):
            batch = await self.extract_urls_recursive(urls_to_crawl)
            urls_to_crawl.clear()
            for url, found_urls in batch:
                results.append((depth, url))
                urls_to_crawl.extend(found_urls)
        return results
