from tqdm import tqdm
import sys
# sys.path.append('/home/wpd/back_fortran')

from gpt_api_base import call_openai
from utils import read_json_list,save_json_list

function_list = read_json_list('./test/test_function.json')
subroutine_list = read_json_list('./test/test_subroutine.json')

function_list = function_list[:3]
subroutine_list = subroutine_list[:3]
function_result_list = []
for data in tqdm(function_list):
    message = [
        {"role": "user", "content": data['instruction'][0]}
    ]
    data["test_result"] = call_openai(message)
    function_result_list.append(data)
save_json_list('./test/GPT4/GPT4_function_test.json', function_result_list)
subroutine_result_list = []
for data in tqdm(subroutine_list):
    message = [
        {"role": "user", "content": data['instruction'][0]}
    ]
    data["test_result"] = call_openai(message)
    subroutine_result_list.append(data)
save_json_list('./test/GPT4/GPT4_subroutine_test.json',subroutine_result_list)

