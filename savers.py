from dataclasses import dataclass
from data_saver import GENERAL_CALLBACK, SPECIAL_CALLBACK

import mariadb


async def __save_print(data: str, filename: str):
    print(f"{filename}: \"{ascii(data)}\"")


async def __save_file(data: str, filename: str):
    with open(filename, "a+") as file:
        file.write(data)


class save_mariadb:

    @dataclass
    class database_type:
        address: str
        ip_type: int
        methodes: List[str]

    def __init__(self, user: str, password: str, host: str, database: str, **kwargs):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.kwargs = kwargs

    def __del__(self):
        try:
            asyncio.run(self.__disconnect())
        except Exception as err:
            pass

    async def __connect(self):
        self.conn = mariadb.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
            **self.kwargs
        )

    async def __disconnect(self):
        try:
            self.conn.commit()
            self.conn.close()
        except Exception as err:
            pass

    async def __save_mariadb(self, data: database_type, filename: str):
        await self.__connect()
        address = data["address"]
        ip_type = data["ip_type"]
        methodes = data["methodes"]
        methodes_str = " ".join(methodes)
        cur = self.conn.cursor(prepared=True)
        cur.callproc(
            'add_proxy', (address, ip_type, methodes_str, filename))
        self.conn.commit()
        await self.__disconnect()

    save_mariadb: SPECIAL_CALLBACK = __save_mariadb


save_file: GENERAL_CALLBACK = __save_file
save_print: GENERAL_CALLBACK = __save_print
