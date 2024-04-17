import json
import re

import utils
def extract_json_from_text(text):
    # 在字符串中使用正则表达式匹配JSON部分
    pattern = r'```json\n(.*?)```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        json_text = match.group(1)
        # 解析 JSON 字符串并返回对象
        return json_text
    else:
        return None
read_list = utils.read_json('./data/fortran/function_filter_result.jsonl')
num = 0
save_list = []
for item in read_list:
    try:
        data = json.loads(extract_json_from_text(item['gpt4_result']))
        if data['result']:
            save_list.append(item)
            num+=1
    except:
        continue
print(num,len(save_list))
utils.save_json('./new_data/fortran/function_filter_result.json',save_list)