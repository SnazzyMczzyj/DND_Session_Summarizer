import openai
import tiktoken
import re
import os


def chunk_calc(prompt):

    prompt = prompt.replace('\n', ' ')      # New lines don't work with the REGEX pattern. 
    text_chunks = [] 
    
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

# If text_chunks is larger than 10 elements, split and add to list_chunk
def chunk_list_split(summary_list):
    
    list_chunk = []
    max_elements = 10

    while len(summary_list) > max_elements:
      list_chunk.append(summary_list[:max_elements])
      summary_list = summary_list[max_elements:]

    if len(summary_list) > 0:
        list_chunk.append(summary_list)

    return list_chunk