#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# openproxy
# parN4Tm#wDzGoPo$wJ%b7DU

from datetime import datetime
import asyncio
from nmapscan import nmapscan
from massscan import masscan
import savers
from data_saver import data_saver


async def main():
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

    masscan = masscan(masscan_executable, scan_file_binary,
                      scan_file_json, scan_file_plain, port, masscan_scan_arguments)
    db = savers.save_mariadb("openproxy", "parN4Tm#wDzGoPo$wJ%b7DU",
                             "home.xosh.fr", "openproxy", autocommit=True)
    savers = data_saver(
        [savers.save_file, savers.save_print], [db.save_mariadb])

    while True:
        try:
            await masscan.start_scan()
            await masscan.transform_output_file()
            masscan_destruct = asyncio.create_task(
                masscan.delete_temporary_files())

            date_time = datetime.today().strftime("%d-%m-%Y_%H-%M-%S")
            nmap_normal_output_file = f"./nmap_scan_{date_time}.txt"
            nmap_xml_output_file = f"./nmap_scan_{date_time}.xml"
            open_proxy_file = f"./open_proxy_{date_time}.txt"
            nmap_scan_arguments = ["-vvv", "-n", "-T4", "--script", "http-open-proxy.nse",
                                   "--open", "-Pn", "-sS"]
            nmap = nmapscan(nmap_executable, savers, scan_file_plain,
                            nmap_xml_output_file, nmap_normal_output_file, open_proxy_file, port, nmap_scan_arguments)
            await nmap.start_scan()
            nmap_get_proxy = asyncio.create_task(nmap.get_open_proxy())
            nmap_destruct = asyncio.create_task(nmap.delete_temporary_files())
            logrotate_task = asyncio.create_task(logrotate(
                [nmap_normal_output_file, nmap_xml_output_file]))
            await asyncio.gather(masscan_destruct, nmap_destruct, nmap_get_proxy, logrotate_task)
        except Exception as err:
            print(err)
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
