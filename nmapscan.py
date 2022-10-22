import subprocess
import xml.dom.minidom as xml
import os
from typing import List, Union
import asyncio
from data_saver import data_saver


class Nmapscan:
    def __init__(self, nmap_exec: str,
                 save: data_saver,
                 input_plain_ip_file_path: str = "./iplist.txt",
                 output_xml_file_path: str = "./nmap-scan.xml",
                 output_plain_file_path: str = "./nmap-scan.txt",
                 output_open_proxy_file_path: str = "./open-proxy.txt",
                 port: int = 3128,
                 scan_parameters=[]):

        self.nmap_exec = nmap_exec
        self.scan_parameters = [*scan_parameters, "-iL", input_plain_ip_file_path,
                                "-oN", output_plain_file_path, "-oX", output_xml_file_path, "-p", str(port)]
        self.input_plain_ip_file_path = input_plain_ip_file_path
        self.output_xml_file_path = output_xml_file_path
        self.output_plain_file_path = output_plain_file_path
        self.output_open_proxy_file_path = output_open_proxy_file_path
        self.save = save

    async def start_scan(self):
        subprocess.call([self.nmap_exec, *self.scan_parameters])

    async def get_open_proxy(self):
        async def parseXml(data: str) -> Union[str, str, str, List[str]] | None:
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
                    return None
                script_output = script_element.getAttribute("output")
                if "GET" in script_output:
                    [_, methode] = script_output.split(":")
                    methode = methode.strip()
                    methodes = methode.split(" ")
                    return (adresse, port, adresse_type, methodes)
            except Exception as err:
                pass
            return None

        data = ""
        record = False
        tasks = []
        with open(self.output_xml_file_path, 'r') as file:
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
                    (adresse, port, adresse_type, methodes) = result
                    ip_type = 4 if "ipv4" in adresse_type else 6
                    data = {
                        "address": adresse,
                        "ip_type": ip_type,
                        "methodes": methodes
                    }
                    save_function = await self.save.special_save(
                        data, self.output_open_proxy_file_path)
                    save_function += await self.save.general_save(
                        str(data), self.output_open_proxy_file_path)
                    tasks += [asyncio.create_task(function())
                              for function in save_function]

                    data = ""
        if len(tasks) != 0:
            asyncio.gather(*tasks)

    async def delete_temporary_files(self):
        try:
            os.remove(self.input_plain_ip_file_path)
            os.remove(self.output_xml_file_path)
            os.remove(self.output_plain_file_path)
        except Exception as err:
            pass
