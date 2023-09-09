import websocket
import base64
import pyaudio
import json
from threading import Thread
from api_secrets import API_KEY_ASSEMBLYAI


YOUR_API_TOKEN = API_KEY_ASSEMBLYAI
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 16000
p = pyaudio.PyAudio()

def on_message(ws, message):
    """
    is being called on every message
    """
    transcript = json.loads(message)
    text = transcript['text']

    if transcript["message_type"] == "PartialTranscript":
        print(f"Partial transcript received: {text}")
    elif transcript['message_type'] == 'FinalTranscript':
        print(f"Final transcript received: {text}")

    pass


def on_error(ws, error):
    """
    is being called in case of errors
    """
    print(error)
    
    pass


def on_open(ws):
    """
    is being called on session start
    """

    def send_data():
        while True:
            # read from the microphone
            data = stream.read(FRAMES_PER_BUFFER)

            # encode the raw data into base64 to send it over the websocket
            data = base64.b64encode(data).decode("utf-8")

            # Follow the message format of the Real-Time service (see documentation)
            json_data = json.dumps({"audio_data":str(data)})


            # Send the data over the wire
            ws.send(json_data)


    # Start a thread where we send data to avoid blocking the 'read' thread
    Thread(target=send_data).start()

    pass


def on_close(ws):
    """
    is being called on session end
    """
    print("WebSocket closed")
    
    pass


# Set up the WebSocket connection with your desired callback functions
websocket.enableTrace(False)

# After opening the WebSocket connection, send an authentication header with your API key
auth_header = {"Authorization": API_KEY_ASSEMBLYAI}

ws = websocket.WebSocketApp(
    f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}",
    header=auth_header,
    on_message=on_message,
    on_open=on_open,
    on_error=on_error,
    on_close=on_close
)


# Start the WebSocket connection
ws.run_forever()



# Real time streaming.
# Split strreaming chunks.