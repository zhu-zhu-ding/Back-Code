import os
from openai import AzureOpenAI


client = AzureOpenAI(
  azure_endpoint = "https://shhnlc2.openai.azure.com/", 
  api_key="7309db19f76d4f0a8d93ac64c1f3aae0",  
  api_version="2024-02-15-preview"
)


message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."}]

completion = client.chat.completions.create(
  model="gpt-4", # model = "deployment_name"
  messages = message_text,
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None
)
print(completion)