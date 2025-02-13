from utils.hashicorp_loader import HashiCorpLoader
from utils.file_encryptor import FileEncryptor
from utils.file_manager import BinaryFileManager
from dotenv import load_dotenv
import os



files_to_del = (
    '../config/.vault',
    '../config/.env.dump'
)

for file in files_to_del:
    try:
        os.remove(file)
    except FileNotFoundError:
        pass


vault_fp = "../config/.vault.enc"
vault_enc = vault_fp.rsplit(".enc")[0]

encryptor = FileEncryptor(
    files_to_encode=[vault_enc],
    binary_file_manager=BinaryFileManager()
)
encryptor.decrypt()
load_dotenv(dotenv_path=vault_enc)

hcp_l = HashiCorpLoader(save_dump=True, folder_to_save_dump="../config/")
res = hcp_l.load(debug=True)



