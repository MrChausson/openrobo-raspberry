#!/usr/bin/env python

from lib.apiclient import ApiClient
from lib.tts import TextToSpeech

client = ApiClient()
tts = TextToSpeech(client)

def main():
    introduction = client.introduce()
    print(introduction)
    tts.speak(introduction)
    return 0

main()