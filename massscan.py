import asyncio
import os
import json
import logging
import aiofiles.os


class Masscan:
    def __init__(self, masscan_exec: str,
                 output_bin_file_path: str = "./masscan-scan-file.bin",
                 output_json_file_path: str = "./masscan-scan-file.json",
                 output_plain_file_path: str = "./masscan-scan-file.txt",
                 port: int = 3128,
                 active_stdout_stderr = (True, True),
                 scan_parameters=[]):
        self.masscan_exec = masscan_exec
        self.output_json_file_path = output_json_file_path
        self.output_bin_file_path = output_bin_file_path
        self.output_plain_file_path = output_plain_file_path
        self.port = port
        self.scan_parameters = [*scan_parameters,
                                "-oB", output_bin_file_path, "-p", str(port)]
        self.logger = logging.getLogger(__file__)
        self.active_stdout_stderr = (
                None if active_stdout_stderr[0] else asyncio.subprocess.PIPE, 
                None if active_stdout_stderr[1] else asyncio.subprocess.PIPE
                )

    def __del__(self):
        try:
            if self.proc.returncode is not None:
                os.kill(self.proc.pid, 9)
        except Exception as err:
            logging.debug(err, stack_info=True)

    async def start_scan(self):
        (p_stdout, p_stderr) = self.active_stdout_stderr
        self.proc = await asyncio.create_subprocess_exec(self.masscan_exec, *self.scan_parameters, stdout=p_stdout, stderr=p_stderr)
        result = await self.proc.wait()
        return result

    async def transform_output_file(self):
        (p_stdout, p_stderr) = self.active_stdout_stderr
        self.proc = await asyncio.create_subprocess_exec(self.masscan_exec, "--readscan", self.output_bin_file_path, "-oJ", self.output_json_file_path, stdout=p_stdout, stderr=p_stderr)
        await self.proc.wait()
        with open(self.output_json_file_path, 'r') as json_file, open(self.output_plain_file_path, 'w+') as plain_file:
            for line in json_file:
                try:
                    data = json.loads(line)
                except Exception as err:
                    self.logger.debug(err, stack_info=True)
                    continue
                plain_file.write(f"{data['ip']}\n")

    async def delete_temporary_files(self):
        try:
            await aiofiles.os.remove(self.output_json_file_path)
            await aiofiles.os.remove(self.output_bin_file_path)
        except Exception as err:
            self.logger.warning(err, stack_info=True)
