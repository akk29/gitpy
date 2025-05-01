import requests, json
class NetworkService:

    def __init__(self, headers=None):
        self.headers = headers

    def get(self, url):
        response = requests.get(url, headers=self.headers)
        return response

    def post(self, url, payload):
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        return response

    def delete(self, url,payload):
        response = requests.delete(url,headers=self.headers, data=json.dumps(payload))
        return response

    def update(self, url, payload):
        response = requests.put(url, headers=self.headers, data=json.dumps(payload))
        return response
