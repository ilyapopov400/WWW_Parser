import time
import aiofiles
import asyncio
import random
import tqdm


async def write_numbers():
    async with aiofiles.open('one_millon_numbers1.txt', mode='a') as file:
        for _ in range(1, 100_000):
            await file.writelines(str(random.randint(10_000, 100_000)) + '\n')


start = time.perf_counter()
asyncio.run(write_numbers())
print(time.perf_counter() - start)


def write_numbers():
    with open('one_millon_numbers2.txt', mode='a') as file:
        for _ in range(1, 100_000):
            file.writelines(str(random.randint(10_000, 100_000)) + '\n')


start = time.perf_counter()
write_numbers()
print(time.perf_counter() - start)
