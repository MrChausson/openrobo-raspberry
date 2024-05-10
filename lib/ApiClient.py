import requests

class ApiClient:
    def __init__(self):
        self.url = "https://openrobo-api.chausson.services"
        self.token = "***REMOVED***"

    def introduce(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.url}/introduce", headers=headers)
        return response.text