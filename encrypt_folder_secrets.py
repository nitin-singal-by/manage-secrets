#!/usr/bin/python
import os
import sys

def _encrypt_secret_files_in(path):
    os.system("./encrypt.sh "+path)

if __name__ == "__main__":
    try:
        secrets_path = sys.argv[1]
        if os.path.exists(secrets_path):
            print("encrypting all secrets located in: ", secrets_path)
            dir_list = os.listdir(secrets_path)
            to_encode = 0
            for file_name in dir_list:
                if file_name.endswith(".secrets"):
                    to_encode = to_encode + 1;
                    _encrypt_secret_files_in(secrets_path+ "/" + file_name)
            if to_encode == 0:
                print("Please ensure there is a file with `.secrets` extension that you wish to encode")   
        else:
            print("Please specify a valid folder name that has secret files to be encrypted.")
    except IndexError:
        print("you need to pass the path to the directory containing the secrets as first argument to this script")
