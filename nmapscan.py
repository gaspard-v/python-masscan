import subprocess
import xml.dom.minidom as xml
import os
from typing import List, Union
import asyncio

class nmapscan:
    def __init__(self, nmap_exec: str, scan_parameters: List[str], input_plain_path: str, output_xml_path: str, output_plain_path: str, output_open_proxy: str):
        self.nmap_exec = nmap_exec
        self.scan_parameters = scan_parameters
        self.input_plain_path = input_plain_path
        self.output_xml_path = output_xml_path
        self.output_plain_path = output_plain_path
        self.output_open_proxy = output_open_proxy
    
    def __del__(self):
        asyncio.run(self.delete_temporary_files())

    async def start_scan(self):
        subprocess.call([self.nmap_exec, *self.scan_parameters,
                        "-iL", self.input_plain_path])

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

    async def delete_temporary_files(self):
        try:
            os.remove(self.input_plain_path)
        except Exception as err:
            pass