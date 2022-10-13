#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio


async def sleep_async():
    await asyncio.sleep(10)
    print("sleep_async done")
    return 10


async def main():
    task = sleep_async()
    print("main done")
    oof = await task
    print(oof)


if __name__ == "__main__":
    asyncio.run(main())
