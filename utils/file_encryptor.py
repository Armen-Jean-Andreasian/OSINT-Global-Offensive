from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from typing import Union, List, Set, Tuple
from . import BinaryFileManager

FilesToEncodeType = Union[List[str], Set[str], Tuple[str]]


class FileEncryptor:
    @staticmethod
    def _initialize_salt():
        def generate_new_salt():
            salt: bytes = os.urandom(16)
            BinaryFileManager.write_file(mode='wb', file_name='salt', data=salt)
            return salt

        try:
            salt = BinaryFileManager.read_file('salt')
        except FileNotFoundError:
            salt = generate_new_salt()
        else:
            if not salt:
                salt = generate_new_salt()
        return salt

    def __init__(
        self,
        files_to_encode: FilesToEncodeType,
        use_salt: bool = False,
    ):
        """
        use_salt:
        - files_to_encode: raw filenames, do not include .enc
        - true: it adds salt that will be saved in a file
        - false: it doesn't add salt, and encrypts using the master key given
        """
        self.files_to_encode = files_to_encode
        _master_key = bytes(input("Enter the key: "), 'utf-8')

        if use_salt:
            salt = self._initialize_salt()
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=480000,
            )

            key = base64.urlsafe_b64encode(kdf.derive(_master_key))
            self._fernet = Fernet(key)
        else:
            key = base64.urlsafe_b64encode(_master_key.ljust(32)[:32])
            self._fernet = Fernet(key)

    def encrypt(self):
        for file_name in self.files_to_encode:
            if os.path.exists(file_name):
                file_data: bytes = BinaryFileManager.read_file(file_name)
                encrypted_data: bytes = self._fernet.encrypt(file_data)
                BinaryFileManager.write_file(file_name=f"{file_name}.enc", data=encrypted_data)
                BinaryFileManager.delete_file(file_name)

    def decrypt(self):
        for file_name in self.files_to_encode:
            file_name_enc = file_name + ".enc"
            if os.path.exists(file_name_enc):
                encrypted_data: bytes = BinaryFileManager.read_file(file_name_enc)
                try:
                    data = self._fernet.decrypt(encrypted_data)
                except InvalidToken:
                    raise ValueError("Key does not match or the file has been tampered with.")
                else:
                    BinaryFileManager.write_file(file_name=file_name, data=data, mode='wb')
                    BinaryFileManager.delete_file(file_name_enc)
            else:
                raise FileNotFoundError(os.path.abspath(file_name_enc), 'wasnt found')
