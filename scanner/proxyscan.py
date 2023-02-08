import threading
import aiohttp
import asyncio

class proxyscan:
    def __init__(self, proxy_list_file: str):
        self.proxy_list_file = proxy_list_file
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        self.test_url = "https://myip.xosh.fr"
        self.lock = threading.Lock()

    async def __test_proxy(self, proxy: str, port: str) -> Tuple[str, str]:
        try:
            port = port.strip()
            proxy = proxy.strip()
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(self.test_url, proxy=f"http://{proxy}:{port}") as response:
                    text = await response.text()
                    text = text.strip()
                    if proxy in text:
                        return (proxy, port)

        except Exception as err:
            pass
        return ("", "")

    async def test_proxies(self):
        tasks = []
        with open(self.proxy_list_file, 'r') as proxy_file:
            for line in proxy_file:
                [proxy, port] = line.split(":")
                task = asyncio.create_task(
                    self.__test_proxy(proxy, port))
                task.add_done_callback(fn)
                tasks.append(task)

        await asyncio.gather(*tasks)