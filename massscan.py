import asyncio
import subprocess
import os
from typing import List
import json

class masscan:
    def __init__(self, masscan_exec: str, 
                    output_bin_file_path: str = "./masscan-scan-file.bin", 
                    output_json_file_path: str = "./masscan-scan-file.json", 
                    output_plain_file_path: str = "./masscan-scan-file.txt",
                    port: int = 3128,
                    scan_parameters: List[str] = []):
        self.masscan_exec = masscan_exec
        self.output_json_file_path = output_json_file_path
        self.output_bin_file_path = output_bin_file_path
        self.output_plain_file_path = output_plain_file_path
        self.port = port
        self.scan_parameters = [*scan_parameters, "-oB", output_bin_file_path, "-p", port]

    async def start_scan(self):
        return subprocess.call([self.masscan_exec, *self.scan_parameters])

    async def transform_output_file(self):
        subprocess.call(
            [self.masscan_exec, "--readscan",
             self.output_bin_file_path, "-oJ", self.output_json_file_path])
        with open(self.output_json_file_path, 'r') as json_file, open(self.output_json_file_path, 'a') as plain_file:
            for line in json_file:
                try:
                    data = json.loads(line)
                except Exception as err:
                    continue
                plain_file.write(f"{data['ip']}\n")

    async def delete_temporary_files(self):
        try:
            os.remove(self.output_json_file_path)
            os.remove(self.output_bin_file_path)
        except Exception as err:
            pass