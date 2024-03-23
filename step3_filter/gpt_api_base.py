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
    # if n==1:
    #     return response["choices"][0]["message"]["content"]
    # else:
    return [result["message"]["content"] for result in  response["choices"]]
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def call_openai_gpt4(message,n=1,temperature=0.8,max_tokens=4096):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=message,
            temperature=temperature,
            max_tokens=max_tokens,
            n=n
        )
        return [result["message"]["content"] for result in response["choices"]]
    except Exception as e:
            print(e)
            return None
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def code_text_similarity(message,n=1,temperature=0.8,max_tokens=4096):
    response = openai.ChatCompletion.create(
        model="code-search-babbage-{doc, query}-001",
        messages=message,
        temperature=temperature,
        max_tokens=max_tokens,
        n=n
    )
    # if n==1:
    #     return response["choices"][0]["message"]["content"]
    # else:
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