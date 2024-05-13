import json

import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt


openai.api_base = "https://api.chatanywhere.com.cn/v1"
openai.api_key = "sk-0X2V2CtOyKgRP0l8VK6howF8X4Rhd2RvCg0i8NBxac6A8Oj6"

api_base = "https://www.jiujiuai.life/v1/chat/completions"
api_key = "sk-31UVgsnLItXrBKQDCa0140EeE73e43B89811028090613197"

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def call_openai(message,n=1,temperature=0.8,max_tokens=4096):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=temperature,
        max_tokens=max_tokens,
        n=n
    )
    if n==1:
        return response["choices"][0]["message"]["content"]
    else:
        return [result["message"]["content"] for result in  response["choices"]]


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def call_api(messages, temperature=0.8,max_tokens=2048):
    url = api_base
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
    data = {
    "model": "gpt-3.5-turbo",
    "messages": messages,
    "max_tokens":max_tokens,
    "temperature":temperature
}
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    reply = response_data['choices'][0]['message']['content']
    total_tokens = response_data['usage']['total_tokens']
    return reply
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def code_text_similarity(text):
    url = "https://api.chatanywhere.com.cn/v1/embeddings"
    headers = {
       'Authorization': 'Bearer sk-0X2V2CtOyKgRP0l8VK6howF8X4Rhd2RvCg0i8NBxac6A8Oj6',
       'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
       'Content-Type': 'application/json'
    }
    data = json.dumps({
   "model": "text-embedding-ada-002",
   "input": text
})
    response = requests.request("POST", url, headers=headers, data=data)
    response_data = response.json()
    # print(response_data)
    return response_data['data'][0]['embedding']

# prompt = """
# You have been asked to act as a logging expert and analyse the given log passages for anomalies. The given log passage is represented as a directed graph. It is given in the following form:(from_node,to_node,weight). from_node denotes the start node, to_node denotes the destination node, and weight denotes the weight. both from_node and to_node are the contents of the logs, and weight denotes the number of times that the next entry in the log corresponding to the from_node is the to_node. node occurrences.
# What you need to pay attention to is: 1. You should not only consider the semantic information of the log content, but also add the structural information.
# 2. an exception is determined only if the log can indicate that the normal operation of the system is affected. You only need to return a Boolean value, True or False. the following is the log content:
# The following is the log information:
# (('instruction cache parity error corrected', 'instruction cache parity error corrected', 49))
# """
# prompt = """
# You have been asked to act as a logging expert and analyse the given log passages for anomalies. The given log passage is represented as a directed graph. It is given in the following form:<from_node> is connected to <to_node>with the weight <weight>.Both from_node and to_node are the contents of the logs, and weight denotes the number of times that the next entry in the log corresponding to the from_node is the to_node. node occurrences.
# What you need to pay attention to is:
# 1. You should consider not only the information about the log content of the graph nodes, but also the information about the weights of the edges of the graph, i.e., the ordering relationships of the logs.
# 2. Returns True only if you can tell that this log indicates that the operation of the system has been affected, otherwise returns False
# You only need to return a Boolean value, True or False.
# The following is the log information:
# <'instruction cache parity error corrected'> is connected to <'instruction cache parity error corrected'> with the weight <49>
# """
# message = [
#         {"role": "user", "content": prompt}
#     ]
# print(call_openai(message))
