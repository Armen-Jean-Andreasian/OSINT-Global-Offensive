import os


class BinaryFileManager:
    @staticmethod
    def read_file(file_name, mode: str = 'rb') -> bytes:
        try:
            with open(file_name, mode=mode) as file:
                file_data = file.read()
            return file_data
        except FileNotFoundError:
            raise FileNotFoundError(f"File wasn't found by: {os.path.abspath(file_name)}")

    @staticmethod
    def delete_file(file_name: str):
        if os.path.isfile(file_name):
            os.remove(file_name)
        else:
            raise FileNotFoundError(file_name)

    @staticmethod
    def write_file(file_name: str, data: bytes | str, mode='wb'):
        with open(file_name, mode) as encrypted_file:
            encrypted_file.write(data)
