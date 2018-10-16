from django.http import JsonResponse
from django.http import HttpResponse
from webcrawler.crawler.imagefinder import ImageFinder
from django.views.decorators.csrf import csrf_exempt
import json
import asyncio
from djangocrawler.logger import log


@csrf_exempt
def crawl(request):
    if request.method == 'OPTIONS':
        response = HttpResponse(status=200)
        return response

    elif request.method == 'POST':
        if request.content_type == 'application/json' and request.body:
                try:
                    request_data = json.loads(request.body)
                    log.info(request_data)
                    seed_url = request_data['seed_url']
                    depth = int(request_data['depth'])
                    result = _start_processing(seed_url, depth)
                    response = JsonResponse(result)
                    return response
                except Exception as e:
                    error = {"status": False,
                             "message" : [e.__str__()],
                             "mandatory parameters" : {"seed_url" : "str",
                                                       "depth": "int"}}
                    return JsonResponse(error,status=500)

        else:
            error = {"message": "Bad Request"}
            return JsonResponse(error,status=400)


def _start_processing(seed_url="",depth=0):
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
    try:
        future = asyncio.Task(img.get_images(main_future.result()), loop=loop)
        loop.run_until_complete(future)
        loop.close()
        result = future.result()
        return result
    except Exception as e:
        log.error("Exception in future : {0}".format(e.__str__()))


