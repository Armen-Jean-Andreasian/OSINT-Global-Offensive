# for development

from utils import FileEncryptor

file = '.env',

encryptor = FileEncryptor(file)

dec = lambda: encryptor.decrypt()
enc = lambda: encryptor.encrypt()

# Your usage below

#dec()
#enc()
