import logging
import logging.handlers
import logging.config
import asyncio
import socket

logging.config.fileConfig('logging.ini')

logger = logging.getLogger(__name__)

async def test():
    while True:
        print("test ok")
        await asyncio.sleep(1)

async def main():
    tasks = []
    while True:
        task = asyncio.create_task(test())
        tasks.append(task)
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        serversocket.bind((socket.gethostname(), 52312))
        # become a server socket
        serversocket.listen()
        serversocket.accept()
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
