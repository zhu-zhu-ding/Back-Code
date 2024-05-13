import json
import os


def read_json(read_path):
    function_list = []
    try:
        with open(read_path, 'r',encoding="utf-8") as jsonl_file:
            for line in jsonl_file:
                json_obj = json.loads(line)
                function_list.append(json_obj)
        return function_list
    except Exception as e:
        print(f"read json_path {read_path} exception:{e}")
        return None

def save_json(save_path,save_list):
    try:
        with open(save_path, 'w', encoding="utf-8") as jsonl_file:
            for save_item in save_list:
                json_string = json.dumps(save_item) + '\n'
                jsonl_file.write(json_string)
            print(f"save data to {save_path}")
    except Exception as e:
        print(f"save json_path {save_path} exception:{e}")

def read_json_list(data_path):
    try:
        return json.load(open(data_path, 'r',encoding="utf-8"))
    except Exception as e:
        print(f"read json_path {data_path} exception:{e}")
        return None
def save_json_list(data_path,data_list):
    try:
        open(data_path, 'w', encoding="utf-8",).write(json.dumps(data_list,indent=4))
    except Exception as e:
        print(f"save json_path {data_path} exception:{e}")
def clear_files():
    for root, dirs, files in os.walk('./'):
        for file in files:
            if file.endswith(".mod") or file.endswith(".f90") or file.endswith(".exe"):
                file_path = os.path.join(root, file)
                os.remove(file_path)