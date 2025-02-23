# for development

from init_container.utils import FileEncryptor
from init_container.utils.file_manager import BinaryFileManager


file = '../config/.env',

encryptor = FileEncryptor(binary_file_manager=BinaryFileManager(), files_to_encode=file)

dec = lambda: encryptor.decrypt()
enc = lambda: encryptor.encrypt()

# Your usage below

#dec()
enc()
