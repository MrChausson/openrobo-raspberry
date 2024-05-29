import requests
import os

class ApiClient:
    def __init__(self):
        self.url = os.getenv("OPENROBO_API_URL")
        # self.url = "http://localhost:8080"
        self.token = os.getenv("OPENROBO_API_TOKEN")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def introduce(self):
        response = requests.get(f"{self.url}/introduce", headers=self.headers)
        return response.text

    def getSpokenText(self, text):
        response = requests.get(f"{self.url}/text-to-speech", headers=self.headers, params={"text": text})
        if (response.status_code == 200):
            return response.content
        else:
            return None

    def Ask(self, text):
        response = requests.get(f"{self.url}/ask", headers=self.headers, params={"question": text, "smiley": "no"})
        return response.text