#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import xml.dom.minidom as xml


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
    # while True:
    #     tasks = []
    #     tasks.append(asyncio.create_task(sleep_async()))
    #     tasks.append(asyncio.create_task(sleep_async_2()))
    #     await asyncio.sleep(5)
    #     print("main done")
    # oof = await asyncio.gather(*tasks)
    # print(oof)
    xml_file = "./open-proxy_13-10-2022_18-21-39.xml"
    oof = ""
    record = False
    with open(xml_file, 'r') as file:
        for line in file:
            if "<host" in line:
                record = True
            if record:
                oof += line
            if "</host>" in line:
                record = False
                dom1 = xml.parseString(oof)
                oof = ""


if __name__ == "__main__":
    asyncio.run(main())
