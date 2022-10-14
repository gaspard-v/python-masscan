#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import os
from datetime import datetime
import tarfile
import asyncio
import sys
from typing import List, Tuple
# import aiohttp
import threading
import xml.dom.minidom as xml


class Proxyscan:
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


class Nmapscan:
    def __init__(self, nmap_exec: str, scan_parameters: List[str], input_plain_path: str, output_xml_path: str, output_plain_path: str, output_open_proxy: str):
        self.nmap_exec = nmap_exec
        self.scan_parameters = scan_parameters
        self.input_plain_path = input_plain_path
        self.output_xml_path = output_xml_path
        self.output_plain_path = output_plain_path
        self.output_open_proxy = output_open_proxy

    async def start_scan(self):
        subprocess.call([self.nmap_exec, *self.scan_parameters,
                        "-iL", self.input_plain_path])

    async def get_open_proxy(self):
        async def parseXml(text):
            try:
                dom = xml.parseString(data)
                [adresse_element] = dom.getElementsByTagName("address")
                [port_element] = dom.getElementsByTagName("port")
                [script_element] = dom.getElementsByTagName("script")
                port = port_element.getAttribute("portid")
                adresse = adresse_element.getAttribute("addr")
                adresse_type = adresse_element.getAttribute("addrtype")
                script_id = script_element.getAttribute("id")
                if not ("http-open-proxy" in script_id):
                    return ""
                script_output = script_element.getAttribute("output")
                if "GET" in script_output:
                    [_, methode] = script_output.split(":")
                    methode = methode.strip()
                    methodes = methode.split(" ")
                    return f"ip: {adresse}, port: {port}, type: {adresse_type}, support: {methode}"
            except Exception as err:
                pass
            return ""

        data = ""
        record = False
        with open(self.output_xml_path) as file:
            for line in file:
                if "<host" in line:
                    record = True
                if record:
                    data += line
                if "</host>" in line:
                    record = False
                    result = await parseXml(data)
                    if result != "":
                        print(result)
                    data = ""

    async def destruct(self):
        try:
            os.remove(self.input_plain_path)
        except Exception as err:
            pass


class Masscan:
    def __init__(self, masscan_exec: str, scan_parameters: List[str], output_bin_path: str, output_json_path: str, output_plain_path: str):
        self.masscan_exec = masscan_exec
        self.scan_parameters = scan_parameters
        self.output_json_path = output_json_path
        self.output_bin_path = output_bin_path
        self.output_plain_path = output_plain_path

    async def start_scan(self):
        return subprocess.call([self.masscan_exec, *self.scan_parameters, "-oB", self.output_bin_path])

    async def transform_output_file(self):
        subprocess.call(
            [self.masscan_exec, "--readscan",
             self.output_bin_path, "-oJ", self.output_json_path])
        with open(self.output_json_path, 'r') as json_file, open(self.output_plain_path, 'a') as plain_file:
            for line in json_file:
                try:
                    data = json.loads(line)
                except Exception as err:
                    continue
                plain_file.write(f"{data['ip']}\n")

    async def destruct(self):
        try:
            os.remove(self.output_json_path)
            os.remove(self.output_bin_path)
        except Exception as err:
            pass


async def logrotate(files: List[str]):
    for file in files:
        try:
            with tarfile.open(f"{file}.tar.xz", 'x:xz') as tar_file:
                tar_file.add(file)
            os.remove(file)
        except FileNotFoundError as err:
            print(f"file {file} not found.\nError message: {err}",
                  file=sys.stderr)
        except Exception as err:
            print(err, file=sys.stderr)


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
    nmap = Nmapscan("nmap_exec", [], "input_plain_path",
                    "./open-proxy_13-10-2022_18-21-39.xml", "output_plain_path", "output_open_proxy")
    await nmap.get_open_proxy()

if __name__ == '__main__':
    asyncio.run(main())
