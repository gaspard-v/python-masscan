#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from nmapscan import Nmapscan
from massscan import Masscan
import savers
from data_saver import data_saver
from utils import logrotate, parse_settings_string
import signal
import logging
import logging.config
import json
import argparse
import os

SIGINT_RECEIVED = False

def sigint_handler(signum, frame):
    global SIGINT_RECEIVED
    if SIGINT_RECEIVED:
        exit(1)
    print("Recieved SIGINT, program is closing...")
    print("press CTRL+C to force the shutdown")
    SIGINT_RECEIVED = True


signal.signal(signal.SIGINT, sigint_handler)

async def parse_arguments():
    default_settings_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json')
    parser = argparse.ArgumentParser(prog="open-proxy", 
                                     description="Search open proxies on the Internet through masscan and nmap", 
                                     epilog="open-proxy scanner")

    parser.add_argument('--settings', 
                        help=f"Specify the settings file, it should be a filepath like \"/path/to/settings.json\". \
                               Default path is \"{default_settings_file}\"",
                        type=argparse.FileType(mode='r', encoding='utf-8'),
                        required=False,
                        default=default_settings_file)
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    return args


async def main():
    global SIGINT_RECEIVED
    script_args = await parse_arguments()
    settings = json.load(script_args.settings)
    logging.config.fileConfig(await parse_settings_string(settings['logging_file']))
    logger = logging.getLogger(__file__)
    masscan_executable = await parse_settings_string(settings['masscan_executable'])

    port = settings['port']
    nmap_executable = await parse_settings_string(settings['nmap_executable'])
    nmap_scan_arguments = ["-n", "-T4", "--script", "http-open-proxy.nse",
                           "--open", "-Pn", "-sS"]
    nmap_scan_arguments += settings["nmap_additional_args"]
    
    mariadb_kwargs = settings['mariadb_kwargs']
    db = savers.save_mariadb(settings['mariadb_user'], settings['mariadb_password'],
                             settings['mariadb_host'], settings['mariadb_database'], **mariadb_kwargs)
    savers_obj = data_saver(
        [savers.save_file], [db.save_mariadb])

    tasks = []

    while not SIGINT_RECEIVED:
        try:
            scan_file_binary = await parse_settings_string(settings['masscan_binary_file'])
            scan_file_json = await parse_settings_string(settings['masscan_json_file'])
            scan_file_plain = await parse_settings_string(settings['masscan_plain_file'])
            blacklist_file = await parse_settings_string(settings['blacklist_file'])
            masscan_scan_arguments = ["--excludefile",
                                    blacklist_file, "--open-only", "--wait", "10", 
                                    "--exclude", "255.255.255.255", "--capture", "html",
                                    "--rate", "1000000", "0.0.0.0/0"]
            masscan_scan_arguments += settings["masscan_additional_args"]
            masscan = Masscan(masscan_executable, scan_file_binary,
                              scan_file_json, scan_file_plain, port, (settings["print_stdout"], settings["print_stderr"]) , masscan_scan_arguments)
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
                            open_proxy_file, port, (settings["print_stdout"], settings["print_stderr"]), nmap_scan_arguments)

            await nmap.start_scan()
            tasks.append(asyncio.create_task(nmap.delete_temporary_files()))
            tasks.append(asyncio.create_task(logrotate([open_proxy_file])))
        except Exception as err:
            logger.exception(err)

    print("finishing all tasks ...")
    await asyncio.gather(*tasks)
    print("done !")

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
