from data_saver import GENERAL_CALLBACK, SPECIAL_CALLBACK, database_type
import mariadb
import logging
import aiofiles
import aiohttp

async def __save_print(data: str, filename: str):
    print(f"{filename}: \"{ascii(data)}\"")


async def __save_file(data: str, filename: str):
    logger = logging.getLogger()
    try:
        async with aiofiles.open(filename, mode="a+") as file:
            await file.write(data)
    except Exception as err:
        logger.warning(err)

class save_api:
    def __init__(self, url, token):
        self.url = url
        self.token = token
    
    
    async def __save_api(self, data: database_type, filename: str):
        logger = logging.getLogger()
        headers={"Authorization": f"Bearer {self.token}"}
        methodes_str = " ".join(data.methodes)
        json_obj = {
            "address": data.address,
            "ip_type": data.ip_type,
            "port": data.port,
            "methodes": methodes_str,
            "scan_date": data.unix_date,
            "commentaire": filename
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(f"{self.url}/proxy/create", json=json_obj) as r:
                json_body = await r.json()
                if r.status != 200 and r.status != 201:
                    logger.error(json_body, stack_info=True)
                # return json_body
            
    save_api: SPECIAL_CALLBACK = __save_api


@DeprecationWarning
class save_mariadb:

    def __init__(self, user: str, password: str, host: str, database: str, **kwargs):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.kwargs = kwargs
        self.logger = logging.getLogger(__file__)

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
            self.logger.warning(err, stack_info=True)

    async def __save_mariadb(self, data: database_type, filename: str):
        try:
            await self.__connect()
            methodes_str = " ".join(data.methodes)
            cur = self.conn.cursor(prepared=True)
            cur.callproc(
                'add_proxy', (data.address, data.port, data.ip_type, methodes_str, data.unix_date, filename))
            self.conn.commit()
            await self.__disconnect()
        except Exception as err:
            self.logger.error(err, stack_info=True)

    save_mariadb: SPECIAL_CALLBACK = __save_mariadb


save_file: GENERAL_CALLBACK = __save_file
save_print: GENERAL_CALLBACK = __save_print
