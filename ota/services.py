import datetime
import os
import glob
from shutil import copy2

from fastapi import HTTPException
from aiofiles.os import remove as async_remove

from ota import settings
from ota.settings import FIRMWARE_DIR


async def get_last_file_from_dir_by_extension(path: str, ext: str):
    result = ''
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file() and entry.name.endswith(f'.{ext}'):
                if entry.name > result:
                    result = entry.name
    return os.path.join(result)


async def get_firmware_path(device_type: str) -> str:
    firmware_dir = os.path.join(FIRMWARE_DIR, device_type)
    return firmware_dir


async def get_last_firmware_info(device_type: str):
    firmware_dir = await get_firmware_path(device_type)
    if not os.path.exists(firmware_dir):
        raise HTTPException(status_code=400, detail=f'Firmware type {device_type} does not exist')
    if not os.path.isdir(firmware_dir):
        raise HTTPException(status_code=400, detail=f'Firmware {device_type} is not a directory')
    current_version_bin_filename = await get_last_file_from_dir_by_extension(firmware_dir, 'bin')
    current_version = os.path.splitext(os.path.basename(current_version_bin_filename))[0]
    return {'bin': current_version_bin_filename, 'version': current_version}


async def get_updated_firmware_version(firmware_type: str):
    source_dir = f"{settings.LATEST_FIRMWARE}/{firmware_type}"
    if not os.path.exists(source_dir):
        raise HTTPException(status_code=400, detail="Source directory not found")
    files = glob.glob(f"{source_dir}/*.bin")
    if not files:
        return True
    source_path = files[0]
    try:
        timestamp = os.path.getmtime(source_path)
        new_name = datetime.datetime.fromtimestamp(timestamp).strftime('%y%m%d%H%M')
        target_path = f"{settings.FIRMWARE_DIR}/{firmware_type}/{new_name}.bin"
        # await async_rename(source_path, target_path)
        copy2(source_path, target_path)
        await async_remove(source_path)

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
