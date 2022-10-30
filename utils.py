import os
from typing import List
import sys
import tarfile
import asyncio
import logging

__logger = logging.getLogger(__file__)

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
            __logger.debug(err, stack_info=True)


async def add_success_callback(fut, callback):
    result = await fut
    await callback()
    return result


def between_callback(callback, args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(callback(args))
    loop.close()
