import openai
import json
import random
import string
import os

def chat_gpt_summary(prompt_chatgpt, summary_list, API_KEY_OPENAI):

  openai.api_key = API_KEY_OPENAI
  
  # Generate random string of text and digits for the file name
  rand_fname = string.ascii_letters+string.digits
  random_filename = ''.join(random.sample(rand_fname, 10))

  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", 
  messages=[
    {"role": "system", "content": "The following text is a transcript of a Dungeons and Dragons session. Summarize the text into 10 points:"},
    {"role": "user", "content": f'{prompt_chatgpt}'}
  ])

  response_message = response['choices'][0]['message']['content']

  folder_name = 'Summaries'
  current_directory = os.path.dirname(os.path.abspath(__file__))
  folder_path = os.path.join(current_directory, folder_name)
  
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)

  if response_message:
      response_filename = 'summary_' + random_filename + '.txt'
      file_path = os.path.join(folder_path, response_filename)
      with open(file_path, 'w') as f:
          f.write(response_message)
      print('(#####) Summary Saved As: ' + response_filename + ' In Summaries File')

  summary_list.append(response_message)
  return summary_list
  
     