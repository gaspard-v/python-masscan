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
from utils import logrotate, add_success_callback
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

async def main():
    global SIGINT_RECEIVED
    masscan_executable = "masscan"
    scan_file_binary = "./masscan-open-proxy.bin"
    scan_file_json = "./masscan-open-proxy.json"
    scan_file_plain = "./masscan-open-proxy.txt"
    blacklist_file = "./ipblacklist.txt"
    port = 3128
    masscan_scan_arguments = ["--excludefile",
                              blacklist_file, "--open-only",
                              "--exclude", "255.255.255.255", "--capture", "html",
                              "--rate", "500000", "0.0.0.0/0"]
    nmap_executable = "nmap"
    nmap_scan_arguments = ["-vvv", "-n", "-T4", "--script", "http-open-proxy.nse",
                           "--open", "-Pn", "-sS"]

    masscan = Masscan(masscan_executable, scan_file_binary,
                      scan_file_json, scan_file_plain, port, masscan_scan_arguments)
    db = savers.save_mariadb("openproxy", "parN4Tm#wDzGoPo$wJ%b7DU",
                             "home.xosh.fr", "openproxy", autocommit=True)
    savers_obj = data_saver(
        [savers.save_file, savers.save_print], [db.save_mariadb])
    
    tasks = []

    while not SIGINT_RECEIVED:
        await masscan.start_scan()
        await masscan.transform_output_file()
        tasks.append(asyncio.create_task(
            masscan.delete_temporary_files()))

        date_time = datetime.today().strftime("%d-%m-%Y_%H-%M-%S")
        nmap_normal_output_file = f"./nmap_scan_{date_time}.txt"
        nmap_xml_output_file = f"./nmap_scan_{date_time}.xml"
        open_proxy_file = f"./open_proxy_{date_time}.txt"

        nmap = Nmapscan(nmap_executable, savers_obj, scan_file_plain,
                        nmap_xml_output_file, nmap_normal_output_file, 
                        open_proxy_file, port, nmap_scan_arguments)

        await nmap.start_scan()
        task = asyncio.ensure_future(nmap.get_open_proxy())
        task = asyncio.ensure_future(add_success_callback(task, nmap.delete_temporary_files()))
        task = asyncio.create_task(add_success_callback(task, logrotate([open_proxy_file])))
        tasks.append(task)

    print("finishing all tasks ...")
    await asyncio.gather(*tasks)
    print("done !")

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
