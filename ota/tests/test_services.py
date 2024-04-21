import tempfile

import pytest

from ota.services import get_last_file_from_dir_by_extension


@pytest.mark.asyncio
async def test_get_last_file_from_dir_by_extension(temp_files):
    max_file = await get_last_file_from_dir_by_extension(temp_files['path'], 'txt')
    assert max_file == max(temp_files['files'])
