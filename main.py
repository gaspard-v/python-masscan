#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import asyncio
from nmapscan import nmapscan
from savers import save_mariadb


async def main():
    # masscan_executable = "masscan"
    # scan_file_binary = "./masscan-open-proxy.bin"
    # scan_file_json = "./masscan-open-proxy.json"
    # scan_file_plain = "./masscan-open-proxy.txt"
    # blacklist_file = "./ipblacklist.txt"
    # masscan_scan_arguments = ["-p", "3128", "--excludefile",
    #                           blacklist_file, "--open-only",
    #                           "--exclude", "255.255.255.255", "--capture", "html",
    #                           "--rate", "500000", "0.0.0.0/0"]
    # nmap_executable = "nmap"

    # while True:
    #     masscan = Masscan(masscan_executable,
    #                       masscan_scan_arguments, scan_file_binary, scan_file_json, scan_file_plain)

    #     await masscan.start_scan()
    #     await masscan.transform_output_file()
    #     masscan_destruct = asyncio.create_task(masscan.destruct())

    #     date_time = datetime.today().strftime("%d-%m-%Y_%H-%M-%S")
    #     nmap_normal_output_file = f"./open-proxy_{date_time}.txt"
    #     nmap_xml_output_file = f"./open-proxy_{date_time}.xml"
    #     nmap_scan_arguments = ["-vvv", "-n", "-T4", "--script", "http-open-proxy.nse", "-p", "3128",
    #                            "--open", "-Pn", "-sS", "-oN", nmap_normal_output_file, "-oX", nmap_xml_output_file]
    #     nmap = Nmapscan(nmap_executable, scan_file_plain,
    #                     nmap_scan_arguments)
    #     await nmap.start_scan()
    #     nmap_destruct = asyncio.create_task(nmap.destruct())
    #     logrotate_task = asyncio.create_task(logrotate(
    #         [nmap_normal_output_file, nmap_xml_output_file]))

    # await asyncio.gather(masscan_destruct, nmap_destruct, logrotate_task)
    db = save_mariadb("openproxy", "parN4Tm#wDzGoPo$wJ%b7DU",
                      "10.66.66.1", "openproxy")
    await db.save_mariadb({"address": "5.5.5.5", "ip_type": 4})

if __name__ == '__main__':
    asyncio.run(main())
