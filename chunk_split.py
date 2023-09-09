import openai
import tiktoken
import re
import os

text_chunks = []


'''
# Test Prompt

current_directory = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(current_directory, 'Test_Files')
file_path = os.path.join(folder_path, 'test_text.txt')
with open(file_path, 'r', encoding='UTF-8') as file:
    prompt = file.read()
print(prompt)
'''

prompt = ''

def chunk_calc(prompt, text_chunks):

    prompt = prompt.replace('\n', ' ')      # New lines don't work with the REGEX pattern.  
    
    remaining_text = None
    max_tokens = 3000       # gpt-3.5-turbo allows 4097 tokens to be shared between the prompt and the response. Max tokens can be adjusted if there needs to be more/less room for a larger/smaller response.
    transcript_text = prompt
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo") 

    while len(encoding.encode(transcript_text)) > 0:
            
        if remaining_text is None:
            remaining_text = encoding.encode(transcript_text)
        
        else:
            remaining_text = remaining_text       
            
        token_length = len(remaining_text)
        
        if token_length > max_tokens:
            encoded_workable_text = remaining_text[:max_tokens]
            decoded_workable_text = encoding.decode(encoded_workable_text)
            
            text_chunk = re.findall(r'^(.*?\.)[^.]*$', decoded_workable_text)
            text_chunks.append(text_chunk)
            
            remaining_text = remaining_text[len(encoding.encode(text_chunk[0])):]

        else:
            decoded_workable_text = encoding.decode(remaining_text)

            text_chunk = decoded_workable_text
            text_chunks.append(text_chunk)

            return text_chunks

            
#chunk_calc(prompt,text_chunks)
#print('Number Of Chunks:', len(text_chunks))
#print('Chunk List:', text_chunks)