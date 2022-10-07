#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import os
from datetime import datetime
import tarfile


class Nmapscan:
    def __init__(self, nmap_exec: str, masscan_output_path: str, scan_parameters: [str]):
        self.nmap_exec = nmap_exec
        self.scan_parameters = scan_parameters
        self.masscan_output_path = masscan_output_path

    def start_scan(self):
        subprocess.call([self.nmap_exec, *self.scan_parameters,
                        "-iL", self.masscan_output_path])

    def destruct(self):
        os.remove(self.masscan_output_path)


class Masscan:
    def __init__(self, masscan_exec: str, scan_parameters: [str], output_bin_path: str, output_json_path: str, output_plain_path: str):
        self.masscan_exec = masscan_exec
        self.scan_parameters = scan_parameters
        self.output_json_path = output_json_path
        self.output_bin_path = output_bin_path
        self.output_plain_path = output_plain_path

    def start_scan(self):
        return subprocess.call([self.masscan_exec, *self.scan_parameters, "-oB", self.output_bin_path])

    def transform_output_file(self):
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

    def destruct(self):
        os.remove(self.output_json_path)


def logrotate(files: [txt]):
    for file in files:
        with tarfile.open(f"{file}.tar.xz", 'x:xz') as tar_file:
            tar_file.add(file)
        os.remove(file)


def main():
    masscan_executable = "masscan"
    scan_file_binary = "./masscan-open-proxy.bin"
    scan_file_json = "./masscan-open-proxy.json"
    scan_file_plain = "./masscan-open-proxy.txt"
    blacklist_file = "./ipblacklist.txt"
    masscan_scan_arguments = ["-p", "3128", "--excludefile",
                              blacklist_file, "--open-only",
                              "--exclude", "255.255.255.255", "--capture", "html",
                              "--rate", "500000", "0.0.0.0/0"]

    while(True):
        masscan = Masscan(masscan_executable,
                          masscan_scan_arguments, scan_file_binary, scan_file_json, scan_file_plain)
        nmap = Nmapscan(nmap_executable, scan_file_plain,
                        nmap_scan_arguments)

        masscan.start_scan()
        masscan.transform_output_file()
        masscan.destruct()

        date_time = datetime.today().strftime("%d-%m-%Y_%H-%M")
        nmap_normal_output_file = f"./open-proxy_{date_time}.txt"
        nmap_xml_output_file = f"./open-proxy_{date_time}.xml"
        nmap_executable = "nmap"
        nmap_scan_arguments = ["-vvv", "-n", "-T4", "--script"
                               "http-open-proxy.nse", "-p", "3128", "--open",
                               "-Pn", "-sS", "-oN", nmap_normal_output_file, "-oX", nmap_xml_output_file]
        nmap.start_scan()
        nmap.destruct()
        logrotate([nmap_normal_output_file, nmap_xml_output_file])


if __name__ == '__main__':
    main()
