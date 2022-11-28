import asyncio
import aiofiles
import aiofiles.os
import os


async def main():

    f_null = open(os.devnull, "w")
    p = await asyncio.create_subprocess_exec("curl.exe", 'www.google.com', stdout=f_null, close_fds=True)
    
    await p.communicate()
    f_null.close()
    p1 = await asyncio.create_subprocess_exec("curl.exe", 'www.google.com', stdout=f_null, close_fds=True)
    await p1.communicate()
    f_null.close()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())