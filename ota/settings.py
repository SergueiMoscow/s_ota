import os
from pathlib import Path
from environs import Env

ROOT_DIR = Path(__file__).parent.parent
env = Env()
env.read_env(str(ROOT_DIR / '.env'))

FIRMWARE_DIR = os.path.join(ROOT_DIR, 'firmware')
LATEST_FIRMWARE = env('LATEST_FIRMWARE')
