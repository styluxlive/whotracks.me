import aiohttp
import asyncio
import async_timeout
import json


async def fetch(session, url):
    with async_timeout.timeout(10):
        try:
            async with session.head(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0'}) as response:
                return {
                    "original_url": url,
                    "status": response.status,
                    "final_url": response.url
                }
        except:
            return {
                "original_url": url,
                "status": 499,  # assigned to exceptions
                "final_url": url
            }


async def fetch_all(session, urls, loop):
    return await asyncio.gather(
        *[loop.create_task(fetch(session, url)) for url in urls]
    )


def retrieve_status(urls):
    async def main(urls, loop):
        conn = aiohttp.TCPConnector(verify_ssl=True) #verify_ssl needs to be true, otherwise it will accept invalid certificates.
        async with aiohttp.ClientSession(connector=conn) as session:
            return await fetch_all(session, urls, loop)

    #https://docs.python.org/3.5/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.set_exception_handler
    def handler(self, context):
        print(context['exception'])
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handler)
    results = loop.run_until_complete(main(urls, loop))
    return results


def write_to_file(filepath, json_output):
    with open(f'{filepath}.json', 'w') as fout:
        json.dump(json_output, fout)
