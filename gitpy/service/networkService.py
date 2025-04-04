import requests, json

DEV_API_V3 = "https://api.github.com"
class NetworkService:

    def __init__(self, headers=None):
        self.headers = headers
        self.loader = 1

    def get(self, url):
        self.base_url = self.get_base_url(url)
        response = requests.get(self.base_url, headers=self.headers)
        return response
    
    def post(self, url, payload):
        self.base_url = self.get_base_url(url)
        response = requests.post(self.base_url, headers=self.headers, data=json.dumps(payload))
        return response

    def delete(self, url):
        self.base_url = self.get_base_url(url)
        response = requests.delete(self.base_url, headers=self.headers)
        return response

    def get_base_url(self, url):
        return f"{DEV_API_V3}/{url}"
