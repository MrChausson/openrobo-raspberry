#!/usr/bin/env python
import json
import requests

def display_stream(response):
    for line in response.iter_lines():
        if line:
            response_json = json.loads(line)
            if 'response' in response_json:
                print(response_json['response'], end='', flush=True)

def main():
    data = '{"model": "phi3", "prompt":"Can you say hello", "stream": true}'
    response = requests.post(url='http://localhost:11434/api/generate', data=data, stream=True)
    display_stream(response)
    
    return 0

main()