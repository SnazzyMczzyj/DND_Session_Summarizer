import requests
from api_secrets import API_KEY_ASSEMBLYAI
import time

from openai_sum import chat_gpt_summary
from api_secrets import API_KEY_OPENAI

from chunk_split import chunk_calc

text_chunks = []
summary_list = []
prompt = ''
 
base_url = 'https://api.assemblyai.com/v2'
headers = {'authorization' : API_KEY_ASSEMBLYAI}

filename = input('Enter File Name: ')
if len(filename) < 1:
    filename = 'test_1.wav'
print("File uploading... \n\nProcessing time takes roughly 15-30% of the file's duration. For example, a 10 minute file takes 90-180 seconds to complete.\n\n")


### upload ###
with open(filename, 'rb') as f:
    response = requests.post(base_url + '/upload',
                             headers = headers,
                             data = f)
    
    upload_url = response.json()['upload_url']


### transcribe ###
print('(#____) Transcribing\n\n')
data = {'audio_url' : upload_url,
        'speaker_labels' : True}    
url = base_url + '/transcript'
response = requests.post(url, json = data, headers = headers)


### polling ###
print('(##___) Polling\n\n')
transcript_id = response.json()['id']
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

while True:
  transcription_result = requests.get(polling_endpoint, headers=headers).json()

  if transcription_result['status'] == 'completed':
    transcript_text = transcription_result['text']
    utterances = transcription_result['utterances']
    
    for utterance in utterances:
       speaker = utterance['speaker']
       text = utterance['text']
       prompt_1 = f'Speaker {speaker}: {text}'
       if prompt:  
        prompt += " "
       prompt += prompt_1

    break

  elif transcription_result['status'] == 'error':
    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

  else:
    time.sleep(10)


### calculate chunks ###
print('(###__) Splitting Chunks\n\n')
chunk_calc(prompt, text_chunks)
#print('Number Of Chunks:', len(text_chunks))
#print('Chunk List:', text_chunks)


### send chunks to chat-gpt ###
print('(####_) Summarizing\n\n')
for i in text_chunks:
   prompt_chatgpt = i
   chat_gpt_summary(prompt_chatgpt, summary_list, API_KEY_OPENAI) #returns summary_list



## Automatically upload them to shared Google drive? ## 
## 