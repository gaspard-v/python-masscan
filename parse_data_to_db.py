#!/usr/bin/env python3


import asyncio
import xml.dom.minidom as xml
from data_saver import data_saver, database_type
import savers
from utils import between_callback
import logging
import logging.config
import os
import threading
import signal

SIGINT_RECEIVED = False


def sigint_handler(signum, frame):
    global SIGINT_RECEIVED
    if SIGINT_RECEIVED:
        exit(1)
    print("Recieved SIGINT, program is closing...")
    print("press CTRL+C to force the shutdown")
    SIGINT_RECEIVED = True


signal.signal(signal.SIGINT, sigint_handler)


async def parse_open_proxy(event):
    async def parseXml(data: str):
        try:
            dom = xml.parseString(data)
            [adresse_element] = dom.getElementsByTagName("address")
            [port_element] = dom.getElementsByTagName("port")
            [script_element] = dom.getElementsByTagName("script")
            [host_element] = dom.getElementsByTagName("host")
            port = port_element.getAttribute("portid")
            adresse = adresse_element.getAttribute("addr")
            adresse_type = adresse_element.getAttribute("addrtype")
            script_id = script_element.getAttribute("id")
            unix_date = host_element.getAttribute("endtime")
            if not ("http-open-proxy" in script_id):
                return None
            script_output = script_element.getAttribute("output")
            if "GET" in script_output:
                [_, methode] = script_output.split(":")
                methode = methode.strip()
                methodes = methode.split(" ")
                ip_type = 4 if "ipv4" in adresse_type else 6
                return (adresse, int(port), ip_type, methodes, int(unix_date))
        except Exception as err:
            logger.debug(err, stack_info=True)
        return None

    db = savers.save_mariadb("openproxy", "parN4Tm#wDzGoPo$wJ%b7DU",
                             "home.xosh.fr", "openproxy", autocommit=True)
    saver = data_saver(
        [savers.save_file, savers.save_print], [db.save_mariadb])
    logger = logging.getLogger("parse_open_proxy")
    output_open_proxy_file_path = "open-proxy.txt"
    output_xml_file_path = "open-proxy_13-10-2022_18-21-39.xml"
    data = ""
    record = False
    tasks = []
    last_file_position = 0
    while not event.is_set():
        try:
            await asyncio.sleep(1)
            try:
                r = open(output_xml_file_path, 'r')
            except Exception as err:
                logger.debug(err, stack_info=True)
                continue
            with r as file:
                file.seek(last_file_position)
                for line in file:
                    if "<host" in line:
                        record = True
                    if record:
                        data += line
                    if "</host>" in line:
                        record = False
                        result = await parseXml(data)
                        if not result:
                            continue
                        (adresse, port, adresse_type,
                         methodes, unix_date) = result
                        data = database_type(
                            adresse, adresse_type, methodes, unix_date, port)
                        save_function = await saver.special_save(
                            data, output_open_proxy_file_path)
                        save_function += await saver.general_save(
                            str(data), output_open_proxy_file_path)
                        tasks += [asyncio.create_task(func)
                                  for func in save_function]

                        data = ""
                last_file_position = file.tell()
        except Exception as err:
            logger.error(err, stack_info=True)
    try:
        await asyncio.gather(*tasks)
    except Exception as err:
        logger.error(err, stack_info=True)


async def main():
    global SIGINT_RECEIVED
    logging.config.fileConfig(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'logging.ini'))
    logger = logging.getLogger(__file__)
    try:
        event = threading.Event()
        thread = threading.Thread(
            target=between_callback, args=(parse_open_proxy, event))
        thread.start()
        while not SIGINT_RECEIVED:
            await asyncio.wait(1)
        event.set()
        thread.join()
    except Exception as err:
        logger.critical(err, stack_info=True)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
