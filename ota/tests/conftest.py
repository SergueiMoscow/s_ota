import os
import tempfile

import pytest


@pytest.fixture
def temp_files(faker):
    count_files = faker.random_int(3, 10)
    temp_dir = tempfile.mkdtemp()
    file_names = []

    try:
        for i in range(count_files):
            filename = f'temp_file_{i}.txt'
            file_path = os.path.join(temp_dir, f'temp_file_{i}.txt')
            with open(file_path, 'w') as file:
                file.write("Temporary file content")
            file_names.append(filename)

        yield {'path': temp_dir, 'files': file_names}

    finally:
        for file_name in file_names:
            os.remove(os.path.join(temp_dir, file_name))
        os.rmdir(temp_dir)
