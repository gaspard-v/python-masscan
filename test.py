import asyncio
import aiofiles.os

async def main():

    tasks = [asyncio.create_task(func) for func in []]
    await asyncio.gather(*tasks)
    try:
        await aiofiles.os.remove("proxyscan.log")
    except Exception as err:
        print(err)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())