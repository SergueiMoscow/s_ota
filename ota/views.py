import os
from http.client import HTTPResponse

from fastapi import APIRouter
from starlette.responses import JSONResponse, FileResponse

from ota.services import get_last_firmware_info, get_firmware_path, get_updated_firmware_version

router = APIRouter()


@router.get('/get_info/{device_type}')
async def get_last_version_info(device_type: str):
    await get_updated_firmware_version(device_type)
    last_version_info = await get_last_firmware_info(device_type)
    return JSONResponse(last_version_info)


@router.get('/get_bin/{device_type}')
async def get_last_version_bin(device_type: str):
    await get_updated_firmware_version(device_type)
    firmware_dir = await get_firmware_path(device_type)
    last_version_info = await get_last_firmware_info(device_type)
    return FileResponse(os.path.join(firmware_dir, last_version_info['bin']))
