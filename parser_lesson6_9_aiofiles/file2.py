import aiofiles
import asyncio
import aiohttp
import time


async def async_write(url):
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open('video/async_video_async.mp4', mode='wb') as video:
            async with session.get(url=url, ssl=False) as response:
                async for piece in response.content.iter_chunked(5120):
                    await video.write(piece)


url = 'https://parsinger.ru/asyncio/aiofile/1/video/nu_pogodi.mp4'

start = time.perf_counter()
asyncio.run(async_write(url=url))
print(time.perf_counter() - start)
