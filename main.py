import requests

from pprint import pprint

response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
APP_ACCESS_TOKEN = response["access_token"]

BASE_URL = "https://api.instagram.com/vi/"

def owner_info():
    r = requests.get(" %susers/self/?access_token = %s "% (BASE_URL,APP_ACCESS_TOKEN)).json()
    if r["meta"]["code"] == 200:
        print "Username is %s" % (r["data"]["username"])
        print "My no. of followers are $s" % (r["data"]["counts"]["followed_by"])
    else:
        print "Status code other than 200 recieved "

    pprint(r)

owner_info()