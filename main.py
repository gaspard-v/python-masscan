#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# openproxy
# parN4Tm#wDzGoPo$wJ%b7DU

from datetime import datetime
import asyncio
from nmapscan import Nmapscan
from massscan import Masscan
import savers
from data_saver import data_saver
from utils import logrotate, parse_settings_string
import signal
import logging
import logging.config
import os
import json

SIGINT_RECEIVED = False


def sigint_handler(signum, frame):
    global SIGINT_RECEIVED
    if SIGINT_RECEIVED:
        exit(1)
    print("Recieved SIGINT, program is closing...")
    print("press CTRL+C to force the shutdown")
    SIGINT_RECEIVED = True


signal.signal(signal.SIGINT, sigint_handler)


async def main():
    global SIGINT_RECEIVED
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json')) as settings_file:
        settings = json.load(settings_file)
    logging.config.fileConfig(os.path.join(os.path.dirname(os.path.realpath(__file__)), await parse_settings_string(settings['logging_file'])))
    logger = logging.getLogger(__file__)
    masscan_executable = await parse_settings_string(settings['masscan_executable'])

    port = settings['port']
    nmap_executable = await parse_settings_string(settings['nmap_executable'])
    nmap_scan_arguments = ["-vvv", "-n", "-T4", "--script", "http-open-proxy.nse",
                           "--open", "-Pn", "-sS"]
    
    mariadb_kwargs = settings['mariadb_kwargs']
    db = savers.save_mariadb(settings['mariadb_user'], settings['mariadb_password'],
                             settings['mariadb_host'], settings['mariadb_database'], **mariadb_kwargs)
    savers_obj = data_saver(
        [savers.save_file, savers.save_print], [db.save_mariadb])

    tasks = []

    while not SIGINT_RECEIVED:
        try:
            scan_file_binary = await parse_settings_string(settings['masscan_binary_file'])
            scan_file_json = await parse_settings_string(settings['masscan_json_file'])
            scan_file_plain = await parse_settings_string(settings['masscan_plain_file'])
            blacklist_file = await parse_settings_string(settings['blacklist_file'])
            masscan_scan_arguments = ["--excludefile",
                                    blacklist_file, "--open-only", "--wait", "10", "-vvv", 
                                    "--exclude", "255.255.255.255", "--capture", "html",
                                    "--rate", "500000", "0.0.0.0/0"]
            masscan = Masscan(masscan_executable, scan_file_binary,
                              scan_file_json, scan_file_plain, port, masscan_scan_arguments)
            masscan_result = await masscan.start_scan()
            logger.debug(f"masscan exited, returned: {masscan_result}")
            await masscan.transform_output_file()
            tasks.append(asyncio.create_task(
                masscan.delete_temporary_files()))

            nmap_normal_output_file = await parse_settings_string(settings['nmap_plain_file'])
            nmap_xml_output_file = await parse_settings_string(settings['nmap_xml_file'])
            open_proxy_file = await parse_settings_string(settings['open_proxy_file'])

            nmap = Nmapscan(nmap_executable, savers_obj, scan_file_plain,
                            nmap_xml_output_file, nmap_normal_output_file,
                            open_proxy_file, port, nmap_scan_arguments)

            await nmap.start_scan()
            tasks.append(asyncio.create_task(nmap.delete_temporary_files()))
            tasks.append(asyncio.create_task(logrotate([open_proxy_file])))
        except Exception as err:
            logger.exception(err, stack_info=True)

    print("finishing all tasks ...")
    await asyncio.gather(*tasks)
    print("done !")

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
