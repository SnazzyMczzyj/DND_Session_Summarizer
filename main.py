from api_secrets import API_KEY_ASSEMBLYAI
from openai_sum import *
from api_secrets import API_KEY_OPENAI
from chunk_split import *
from assembly_ai_functions import *
 
base_url = 'https://api.assemblyai.com/v2'
headers = {'authorization' : API_KEY_ASSEMBLYAI}

filename = input('Enter File Name: ')
if len(filename) < 1:
    filename = 'test.wav'
print("File uploading... \n\nProcessing time takes roughly 15-30% of the file's duration. For example, a 10 minute file takes 90-180 seconds to complete.\n\n")
#                            ^ Calculate estimated time to proccess using the length of the file. 

upload_url = upload_file(filename)

prompt = transcribe_audio(upload_url)

print('(##___) Splitting Chunks\n\n')
text_chunks = chunk_calc(prompt)

print('(###__) Summarizing\n\n')
for i in text_chunks:
   prompt_chatgpt = i
   summary_list = chat_gpt_summary(prompt_chatgpt, API_KEY_OPENAI)

list_chunk = chunk_list_split(summary_list) # returns list_chunk. list_chunk is a chunk of 13 summary lists which is about 3000 tokens. 

for i in list_chunk:
  sum_chunk = i
  sum_of_sum(sum_chunk, API_KEY_OPENAI)