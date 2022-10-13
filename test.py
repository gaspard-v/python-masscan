#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio


async def sleep_async():
    for i in range(15):
        await asyncio.sleep(0.5)
        print("sleep_async done")
    return 10


async def sleep_async_2():
    for i in range(15):
        await asyncio.sleep(0.5)
        print("sleep_async_2 done")
    return 2


async def main():
    while True:
        tasks = []
        tasks.append(asyncio.create_task(sleep_async()))
        tasks.append(asyncio.create_task(sleep_async_2()))
        await asyncio.sleep(5)
        print("main done")
    oof = await asyncio.gather(*tasks)
    print(oof)


if __name__ == "__main__":
    asyncio.run(main())
