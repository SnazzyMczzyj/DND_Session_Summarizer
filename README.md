DND_Session_Summarizer

Upload:
    Move your upload file to the same folder as main.py.

Chunk Tuning:
    Maximum chunk sizes can be modified and chunk models can be changed. 
    I used tiktoken https://pypi.org/project/tiktoken/. 
    Read the tiktoken docs and change the encoding model from gpt-3.5-turbo if needed.

Summaries:
    A summaries file will be created if it does not exixt.
    This will save all the summary chunks as well as the final summary at the end. You can use the summary chunks to experiment with different chatgpt prompts.
    