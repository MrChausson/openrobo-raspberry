#!/usr/bin/env python

from lib.apiclient import ApiClient
from lib.tts import TextToSpeech
from lib.whisper_processor import process_audio
from lib.recording import Recording  # Assuming the Recording class is in the lib.recording module
import os

client = ApiClient()
tts = TextToSpeech(client)

def main():
    introduction = client.introduce()
    print(introduction)
    # tts.speak(introduction)
    try:
        # Create a Recording instance
        # Use keyboard input for debugging
        recorder = Recording()

        # Wait for user to record audio
        print("Press the 'a' key to start recording, then press it again to stop.")
        input("")
        audio_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "audio/recording.wav")
        # Convert from 48kz to 16kz
        recorder.convert_sample_rate()
        result = process_audio(audio_file_path, "base.en")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
    return 0

main()