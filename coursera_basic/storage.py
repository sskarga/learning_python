# Key-value хранилище
# Запись значения по ключу storage.py --key key_name --val value
# Получение значения по ключу storage.py --key key_name

import os
import os.path
import tempfile
import argparse
import json

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

def create_parser():
    """create parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", help="input key", required=True)
    parser.add_argument("-v", "--val", help="value")
 
    return parser.parse_args()

def json_file_load(path_to_file):
    """Load dictionarie from json file"""
    if os.path.isfile(path_to_file):
        try:
            with open(path_to_file, 'r') as f:
                return json.loads(f.read())     
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # File not found or empty, use a default container
            return {}   
    else:
        # File not found use a default container
        return {}

def json_file_save(dict, path_to_file):
    """Save dictionarie to json file"""
    with open(path_to_file, 'w') as f:
        f.write(json.dumps(dict))

if __name__ == '__main__':
    args = create_parser()
    key_val_dict = json_file_load(storage_path)
    val_list = key_val_dict.get(args.key)

    if args.val:
        if val_list == None:
            key_val_dict[args.key] = [args.val]
        else:
            val_list.append(args.val)

        json_file_save(key_val_dict, storage_path)
    else:
        print(*val_list, sep=', ')