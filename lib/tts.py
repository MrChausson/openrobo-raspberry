from lib.apiclient import ApiClient
from pydub import AudioSegment
from pydub.playback import play
import io

class TextToSpeech:
    def __init__(self, apiclient: ApiClient):
        self.client = apiclient

    def speak(self, text):
        audio = self.client.getSpokenText(text)
        
        # Create a BytesIO object and load the audio into it
        audio_io = io.BytesIO(audio)
        
        # Load the audio as an AudioSegment
        audio_segment = AudioSegment.from_file(audio_io, format="mp3")
        
        # Play the audio
        play(audio_segment)