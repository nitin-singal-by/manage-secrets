#!/usr/bin/python
import sys
import os


def _decrypt_all_files(path):
    files = os.listdir(path)
    for f in files:
        input_file = os.path.join(path, f)
        output_file = os.path.join(path, os.path.splitext(f)[0])
        cmd = "gpg -o " + output_file + " -d " + input_file
        os.system(cmd)


def populate_secrets():
    try:
        secrets_path = sys.argv[1]
        print("decrypting all credentials located in: ", secrets_path)
        _decrypt_all_files(secrets_path)
        # Iterate through all secret files and expose the env variables. If two files have the same env variable then it would be overriden.
        dir_list = os.listdir(secrets_path)
        to_decode = 0
        for file_name in dir_list:
            if file_name.endswith(".secrets"):
                env_vars = {}
                with open(secrets_path + "/" + file_name) as secret_file:
                    for line in secret_file:
                        if line.startswith("#") or ":" not in line:
                            skipped = True
                        else:
                            name, var = line.partition(":")[::2]
                            env_vars[name.strip()] = var
            return env_vars
    except IndexError:
        print("you need to pass the path to the directory containing the secrets as first argument to this script")

if __name__ == "__main__":
    envs = populate_secrets()
    print(envs)
    

