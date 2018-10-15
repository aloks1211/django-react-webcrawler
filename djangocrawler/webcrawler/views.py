from django.http import JsonResponse
from webcrawler.crawler.imagefinder import ImageFinder
from django.views.decorators.csrf import csrf_exempt
import json
import asyncio
from djangocrawler.logger import log


@csrf_exempt
def crawl(request):
    if request.method == 'POST':
        if request.content_type == 'application/json' and request.body:
                try:
                    request_data = json.loads(request.body)
                    seed_url = request_data['seed_url']
                    depth = request_data['depth']
                    result = _start_processing(seed_url,depth)
                    return JsonResponse(result)
                except Exception as e:
                    error = {"status": False,
                             "message" : [e.__str__()],
                             "mandatory parameters" : {"seeed_url" : "str",
                                                       "depth": "int"}}
                    return JsonResponse(error,status=400)


def _start_processing(seed_url="",depth=""):
    """

    :param seed_url:
    :param depth:
    :return:
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    img = ImageFinder(seed_url, depth, loop)
    main_future = asyncio.Task(img.start_crawling(), loop=loop)
    loop.run_until_complete(main_future)
    future = asyncio.Task(img.get_images(main_future.result()), loop=loop)
    loop.run_until_complete(future)
    loop.close()
    result = future.result()
    return result

