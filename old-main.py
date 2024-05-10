#!/usr/bin/env python
import json
import os
from playsound import playsound
import requests

def display_stream(response):
    for line in response.iter_lines():
        if line:
            response_json = json.loads(line)
            if 'response' in response_json:
                text = response_json['response']
                print(text, end='', flush=True)
                
                # Speak the response
                directory = "/home/melio/rp-main/piper"
                model = "en_US-lessac-medium"
                os.system(f"echo '{text}' | piper --model {model} --output_file {directory}/welcome.wav")
                playsound(directory + "/welcome.wav")

def main():
    data = '{"model": "phi3", "prompt":"Can you say hello", "stream": true}'
    response = requests.post(url='http://localhost:11434/api/generate', data=data, stream=True)
    display_stream(response)
    
    return 0

main()