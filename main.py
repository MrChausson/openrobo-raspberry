#!/usr/bin/env python

from lib.apiclient import ApiClient
from lib.tts import TextToSpeech
from lib.whisper_processor import process_audio
from lib.recording import Recording
from termcolor import colored
import os

client = ApiClient()
tts = TextToSpeech(client)

def main():
    introduction = client.introduce()
    print(introduction)
    tts.speak(introduction)
    recorder = Recording()
    while True:  # Add a while loop to allow the user to make multiple recordings
        try:
            # Wait for user to record audio
            print("Press the 'a' key to start recording, then press it again to stop.")
            recorder.recording_done.wait()
            audio_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "audio/recording.wav")
            # Convert from 48kz to 16kz
            recorder.convert_sample_rate()
            result = process_audio(audio_file_path, "base.en")
            print(colored("You said: " + result, 'green'))
            ai_answer = client.Ask(result)
            print(colored("Robot answer: " + ai_answer, 'blue'))
            tts.speak(ai_answer)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            recorder.reset()  # Reset the recorder after each recording

    return 0

main()