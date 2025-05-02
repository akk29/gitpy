import requests, json
class NetworkService:

    def __init__(self, headers=None):
        self.session = requests.Session()
        self.session.headers.update(headers)

    def get(self, url):
        response = self.session.get(url)
        return response

    def post(self, url, payload):
        response = self.session.post(url, data=json.dumps(payload))
        return response

    def delete(self, url,payload):
        response = self.session.delete(url, data=json.dumps(payload))
        return response

    def update(self, url, payload):
        response = self.session.put(url, data=json.dumps(payload))
        return response