import asyncio

async def main():

    tasks = [asyncio.create_task(func) for func in []]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())