import datetime
import os
import glob
import logging
import time
import pytz
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
    """
    Возвращает строку версии файла в формате YYMMNDD_HH
    :param firmware_type: Switch, Thermometer, Thermostat, etc.
    :return:
    """
    source_dir = f"{settings.LATEST_FIRMWARE}/{firmware_type}"
    if not os.path.exists(source_dir):
        raise HTTPException(status_code=400, detail="Source directory not found")
    files = glob.glob(f"{source_dir}/*.bin")
    if not files:
        return True
    source_path = files[0]
    try:
        timestamp = os.path.getmtime(source_path)

        # Переводим время на московское
        dt = datetime.datetime.fromtimestamp(timestamp)
        moscow_tz = pytz.timezone('Europe/Moscow')
        moscow_time = dt.astimezone(moscow_tz)
        new_name = moscow_time.strftime('%y%m%d_%H')

        # Это версия с временем ОС
        # new_name = datetime.datetime.fromtimestamp(timestamp).strftime('%y%m%d_%H')

        target_path = f"{settings.FIRMWARE_DIR}/{firmware_type}/{new_name}.bin"
        # await async_rename(source_path, target_path)
        copy2(source_path, target_path)
        await async_remove(source_path)

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


async def write_list_to_log_file(caption: str, values: dict):
    logging.basicConfig(level=logging.INFO, filename='requests.log', filemode='w')
    logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' === ' + caption)
    for key, value in values.items():
        logging.info(f'{key}: {value}')
