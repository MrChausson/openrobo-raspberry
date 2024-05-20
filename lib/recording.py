import os
import numpy as np
import scipy.io.wavfile as wav
import threading
from pynput import keyboard
import pyaudio
import librosa
import soundfile as sf


class Recording:
    def __init__(self):
        self.fs = 48000  # Sample rate
        self.recording = np.array([])
        self.is_recording = False
        self.key = "a"
        self.audio_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../audio/recording.wav")
        self.p = pyaudio.PyAudio()

        # # Choose a specific microphone device
        # device_index = None
        # for i in range(self.p.get_device_count()):
        #     device_info = self.p.get_device_info_by_index(i)
        #     if 'Arctis Nova 7 Mono' == device_info['name']:  # Use your microphone's name
        #         device_index = i
        #         break

        # if device_index is None:
        #     raise Exception("Microphone not found")

        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.fs, input=True, frames_per_buffer=1024)#, input_device_index=device_index)

        # Setup keyboard listener
        listener = keyboard.Listener(
            on_press=self.key_pressed,
            on_release=self.key_released)
        listener.start()

    def record_audio(self):
        print("Start recording")
        self.recording = np.zeros(self.fs * 10, dtype=np.int16)  # Preallocate 10 seconds of audio
        recording_length = 0
        while self.is_recording:
            # Record for 1 second at a time
            for _ in range(0, int(self.fs / 1024)):
                data = self.stream.read(1024)
                new_data = np.frombuffer(data, dtype=np.int16)
                if recording_length + len(new_data) > len(self.recording):
                    # If the recording array is full, double its size
                    self.recording = np.concatenate((self.recording, np.zeros_like(self.recording)))
                self.recording[recording_length:recording_length + len(new_data)] = new_data
                recording_length += len(new_data)
        print("Recording finished")
        # Save as WAV file
        wav.write(self.audio_file_path, self.fs, self.recording[:recording_length].astype(np.int16))

    def key_pressed(self, key):
        try:
            key_char = key.char if hasattr(key, 'char') else None
            if key_char == self.key:
                if self.is_recording:
                    self.is_recording = False
                else:
                    self.is_recording = True
                    threading.Thread(target=self.record_audio).start()
        except AttributeError:
            pass  # Non-character key was pressed

    def key_released(self, key):
        pass  # Do nothing on key release


    def convert_sample_rate(self):
        # Load the audio file with the original sample rate
        y, sr = librosa.load(self.audio_file_path, sr=self.fs)

        # Resample the audio to 16 kHz
        y_resampled = librosa.resample(y, orig_sr=sr, target_sr=16000)

        # Save the resampled audio
        sf.write(self.audio_file_path, y_resampled, 16000)