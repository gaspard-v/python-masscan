#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import os


class Nmapscan:
    def __init__(self, nmap_exec: str, masscan_output_map: object, scan_parameters: [str]):
        self.nmap_exec = nmap_exec
        self.scan_parameters = scan_parameters
        self.temporary_scan_file = "./tmp_nmap.txt"

    def start_scan(self):
        for ip in self.masscan_output_map["ip"]:
            with open(self.temporary_scan_file, 'a') as temporary_file:
                temporary_file.write(ip + "\n")
        subprocess.call([self.nmap_exec, *self.scan_parameters,
                        "-iL", self.temporary_scan_file])

    def destruct():
        os.remove(self.temporary_scan_file)


class Masscan:
    def __init__(self, masscan_exec: str, scan_parameters: [str], output_bin_path: str, output_json_path: str):
        self.masscan_exec = masscan_exec
        self.scan_parameters = scan_parameters
        self.output_json_path = output_json_path
        self.output_bin_path = output_bin_path

    def start_scan(self):
        return subprocess.call([self.masscan_exec, *self.scan_parameters, "-oB", self.output_bin_path])

    def get_output_file(self):
        subprocess.call(
            [self.masscan_exec, "--readscan",
             self.output_bin_path, "-oJ", self.output_json_path])
        with open(self.output_json_path, 'r') as json_file:
            return json.load(json_file)

    def destruct():
        os.remove(output_json_path)


def main():
    masscan_executable = "masscan"
    scan_file_binary = "./masscan-open-proxy.bin"
    scan_file_json = "./masscan-open-proxy.json"
    blacklist_file = "./ipblacklist.txt"
    masscan_scan_arguments = ["-p", "3128", "--excludefile",
                              blacklist_file, "--open-only",
                              "--exclude", "255.255.255.255", "--capture", "html",
                              "--rate", "500000", "0.0.0.0/0"]

    masscan = Masscan(masscan_executable,
                      masscan_scan_arguments, scan_file_binary, scan_file_json)
    # masscan.start_scan()
    masscan_output_object = masscan.get_output_file()
    masscan.destruct()

    nmap_normal_output_file = "./open-proxy.txt"
    nmap_xml_output_file = "./open-proxy.xml"
    nmap_executable = "nmap"
    nmap_scan_arguments = ["-vvv", "--script",
                           "http-open-proxy.nse", "-p", "3128", "--open"
                           "-Pn", "-sS", "-oN", nmap_normal_output_file, "-oX", nmap_xml_output_file]
    nmap = Nmapscan(nmap_executable, masscan_output_object,
                    nmap_scan_arguments)
    nmap.start_scan()
    nmap.destruct()


if __name__ == '__main__':
    main()
