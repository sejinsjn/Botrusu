import requests
class dhook:
    def sendmsg(url, msg, avatar, name):
        json = {
            'content': msg,
            'avatar_url': avatar,
            'username': name
        }
        requests.post(url, json = json)
    def delhook(url):
        requests.delete(url)
    def patchhook(url, name, avatar):
        json = {
            'name': name,
            'avatar': avatar
        }
        requests.patch(url, json=json)