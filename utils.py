import os
from typing import List
import sys
import tarfile

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
    
async def add_success_callback(fut, callback):
    result = await fut
    await callback()
    return result
