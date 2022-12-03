import asyncio
import aiofiles
import aiofiles.os
import random
import string


async def create_random_file():
    letters = string.ascii_lowercase
    result_str = ""
    for i in range(100000):
            result_str += ''.join(random.choice(letters) for i in range(15)) + '\n'
    async with aiofiles.open("test.txt", "w+") as file:
        await file.write(result_str)
        

async def main():
    async def oof(owo):
        owo += "o"
        return (3, owo)
    owo = "i"
    for i in range(5):
        (_, owo) = await oof(owo)
        print(owo)
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())