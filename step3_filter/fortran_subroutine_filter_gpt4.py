from tqdm import tqdm
import json
import utils
from gpt_api_base import code_text_similarity,call_openai_gpt4
import numpy as np
read_path = './data/fortran/instruction_subroutine_result.jsonl'
save_path = './data/fortran/subroutine_filter_result.jsonl'

# def set_prompt():
#     return f"""As a verilog expert, you need to solve the following tasks. Given a code generation benchmark data consisting of detailed functional description instructions and corresponding function code segments, you need to determine whether it meets the requirements of the benchmark data. You need to make the judgment based on the following rules.
#     1. The code has a logical function, not a simple variable assignment.
#     2. The instruction can completely describe the logical function of the code, it can be short or detailed, but it must meet the logical function of the code.
#     3. Code and instructions can be composed of a reasonable benchmark test data, with verilog domain characteristics.
#     Please return a json object containing the following keys, result and reason, result is a boolean value, True means that it meets the requirements, False means that it does not meet the requirements, reason is the reason for making the judgment.
#         """

def set_prompt():
    return f"""
    As a fortran expert, you need to solve the following tasks. Given a list of instructions and function codes describing the function of the code, you need to determine whether there are instruction-code pairs that can all meet the following requirements based on the following rules.

    1. The code must have both input parameters and output parameters; it is an error to have only input parameters or output parameters, and it is also an error to have no input parameters or output parameters at the same time.The instruction must also indicate the input parameters and output parameters.
    2. The code has a logical function and is not a simple variable assignment. 
    3. The instruction can completely describe the logical function of the code, either briefly or in detail, but it must fulfill the logical function of the code.
    4. The code and instructions have fortran domain characteristics.
    Please return a json object containing the following keys, result , instruction, code, reason, result is a boolean value, True means it exists, False means it doesn't exist, instruction is the instruction that meets the condition, code is the code that meets the condition, reason is the reason for making the judgment.
    You need to note that the following rules must all be met.If one of the rules does not match, result returns false and instruction and code are set to empty strings

            """
import json

def gen_message(fortran_code,instruction):
    data = {
        "function_code":fortran_code,
        "instruction":instruction
    }
    data = json.dumps(data)

    message = [
        {"role": "system", "content": data},
        {"role": "user", "content": set_prompt()},
    ]
    return message
def main():
    data_list = utils.read_json(read_path)
    # data_list = data_list[:3]
    save_list = []
    writer = open(save_path, 'w', encoding='utf-8')
    for data in tqdm(data_list):
        instruction = data['instruction']
        function_code = data['code']
        messsage = gen_message(function_code,instruction)
        gpt4_result = call_openai_gpt4(message=messsage,temperature=0)
        writer.write(json.dumps({'data':data,'gpt4_result':gpt4_result.choices[0].message.content})+'\n')
        writer.flush()
        # gpt4_result = call_openai_gpt4(message=messsage,temperature=0)[0]
        # try:
        #     gpt4_result = json.loads(gpt4_result)
        #     save_list.append({'data':data,'gpt4_result':gpt4_result})
        # except:
        #     continue
    utils.save_json(save_path=save_path,save_list=save_list)
    # print(similarity_score)
if __name__ == "__main__":
    main()