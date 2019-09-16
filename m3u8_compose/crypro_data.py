from Crypto.Cipher import AES
import os

def get_decrypt_key(key_path):
    key_file = open(key_path, mode = 'r', encoding='UTF-8')
    key_data = key_file.read()
    cryptor = AES.new(key_data.encode('utf-8'), AES.MODE_CBC)
    key_file.close()
    return cryptor




def decrypt(file_path, cryptor):
    old_file = open(file_path ,mode = 'rb')
    data = old_file.read()
    old_file.close()
    (current_dir, file_name) = os.path.split(file_path)
    current_dir = current_dir + "_new"
    if not os.path.exists(current_dir):
        os.mkdir(current_dir)
    apth = os.path.join(current_dir,file_name)
    with open(apth, 'ab') as new_file:
        new_file.write(cryptor.decrypt(data))
    new_file.close()
