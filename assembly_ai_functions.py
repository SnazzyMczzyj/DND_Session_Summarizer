import requests
from api_secrets import API_KEY_ASSEMBLYAI
import time
 
base_url = 'https://api.assemblyai.com/v2'
headers = {'authorization' : API_KEY_ASSEMBLYAI}

filename = input('Enter File Name: ')
if len(filename) < 1:
    filename = 'test.wav'
print("File uploading... \n\nProcessing time takes roughly 15-30% of the file's duration. For example, a 10 minute file takes 90-180 seconds to complete.\n\n")
#                            ^ Calculate estimated time to proccess using the length of the file. 


def upload_file(filename):
  with open(filename, 'rb') as f:
      response = requests.post(base_url + '/upload',
                              headers = headers,
                              data = f)
      
      upload_url = response.json()['upload_url']
      return upload_url


# Use text replace in Assembly AI to fix wrong spellings. 
def transcribe_audio(upload_url):
  print('(#____) Transcribing\n\n')
  data = {'audio_url' : upload_url,
          'speaker_labels' : True}    
  url = base_url + '/transcript'
  response = requests.post(url, json = data, headers = headers)


  transcript_id = response.json()['id']
  polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

  prompt = ''

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

      return prompt

    elif transcription_result['status'] == 'error':
      raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

    else:
      time.sleep(10)