import openai
import json
import random
import string
import os

def chat_gpt_summary(prompt_chatgpt, API_KEY_OPENAI):

  summary_list = []

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
      print('(####_) Summary Saved As: ' + response_filename + ' In Summaries File')

  summary_list.append(response_message.replace("/n", " "))
  
  return summary_list


def sum_of_sum(sum_chunk, API_KEY_OPENAI):

  openai.api_key = API_KEY_OPENAI

  rand_fname = string.ascii_letters+string.digits
  random_filename = ''.join(random.sample(rand_fname, 10))

  full_response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
    messages=[
      {"role": "system", "content": "The following prompt is a list of summary points from a single Dungeons and Dragons session. The points may be numbered, but they are all from the same session. The points are in chronological order, regardless of their numbers. Summarize the points into a complete and finished detailed story that is mainly informational."}, 
      {"role": "user", "content": f'{sum_chunk}'}
    ])

  summary_response_message = full_response['choices'][0]['message']['content']

  folder_name = 'Summaries'
  current_directory = os.path.dirname(os.path.abspath(__file__))
  folder_path = os.path.join(current_directory, folder_name)

  if not os.path.exists(folder_path):
      os.makedirs(folder_path)

  if summary_response_message:
      full_response_filename = 'final_summary_' + random_filename + '.txt'
      file_path = os.path.join(folder_path, full_response_filename)
      with open(file_path, 'w') as f:
          f.write(summary_response_message)
      print('(#####) Final Summary Saved As: ' + full_response_filename + ' In Summaries File')