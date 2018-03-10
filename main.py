import requests
import urllib
from pprint import pprint
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#importing lib

response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
APP_ACCESS_TOKEN = response['access_token']
print response


BASE_URL = "https://api.instagram.com/vi/"

#saving base url in variable

def owner_info():
    r = requests.get(" %susers/self/?access_token = %s "% (BASE_URL,APP_ACCESS_TOKEN)).json()
    if r["meta"]["code"] == 200:
        print "Username is %s" % (r["data"]["username"])
        print "No. of followers are $s" % (r["data"]["counts"]["followed_by"])
        print "No. of people you are following: %s" % (r["data"]["counts"]["follows"])
        print "No. of posts: %s" % (r["data"]["counts"]["media"])
    else:
        print "Status code other than 200 recieved "

    pprint(r)

#getting owners information function


def owner_post():
    r = requests.get(" %susers/self/media/recent/?access_token = %s "% (BASE_URL,APP_ACCESS_TOKEN)).json()
    if r["meta"]["code"] == 200:
        #pprint(r)
        url =  r["data"][0]["images"]["standard_resolution"]["url"]
        name = r["data"][0]["id"] + "jpg"
        urllib.urlretrieve(url,name)
        print "Your image is downloaded"
    else:
        print "Status code other than 200 recieved "

#downloading and viewing the post

def get_user_id(uname):
    r = requests.get("%susers/search?q=%s&access_token=%s"%(BASE_URL,uname,APP_ACCESS_TOKEN)).json()
    return r["data"][0]["id"]


def user_info(uname):
    user_id = get_user_id(uname)
    r = requests.get(" %susers/%s/?access_token = %s " % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if r["meta"]["code"] == 200:
        print "Username is %s" % (r["data"]["username"])
        print "No. of followers are $s" % (r["data"]["counts"]["followed_by"])
        print "No. of people you are following: %s" % (r["data"]["counts"]["follows"])
        print "No. of posts: %s" % (r["data"]["counts"]["media"])
    else:
        print "Status code other than 200 recieved "

    pprint(r)

def user_post(username):
    user_id = get_user_id(username)
    r = requests.get(" %susers/%s/media/recent/?access_token = %s " % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if r["meta"]["code"] == 200:
        #pprint(r)
        print r["data"][0]["images"]["standard_resolution"]["url"]
        url = r["data"][0]["images"]["standard_resolution"]["url"]
        name = r["data"][0]["id"] + "jpg"
        urllib.urlretrieve(url, name)
        print "Your image is downloaded"
    else:
        print "Status code other than 200 recieved "

def get_media_id(uname):
    user_id = get_user_id(uname)
    r = requests.get(" %susers/%s/media/recent/?access_token = %s " % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
    if r["meta"]["code"] == 200:
       return r["data"][0]["id"]
    else:
        print "Status code other than 200 recieved "



def like_post(uname):
    media_id = get_user_id(uname)
    payload = {"access_token": APP_ACCESS_TOKEN}
    url = BASE_URL + "media/%s/likes" % (media_id)
    r = requests.post(url , payload).json()
    if r["meta"]["code"]==200:
        print "Like Successful"
    else:
        print "Like Unsuccessful"
#liking the post


def comment_post(uname):
    media_id = get_media_id(uname)
    comment = raw_input("What is your comment? ")
    payload = {"access_token": APP_ACCESS_TOKEN , "text": comment}
    url = BASE_URL + "media/%s/comments" % (media_id)
    r = requests.post(url, payload).json()
    if r["meta"]["code"] == 200:
        print "Comment Successful"
    else:
        print "Comment Unsuccessful"

#commenting on the post

def del_comment(uname):
    media_id = get_user_id(uname)
    r = requests.get("%smedia/%s/comments?access_token=%s" %(BASE_URL,media_id,APP_ACCESS_TOKEN)).json()
    if r["meta"]["code"]==200:
        if len(r["data"])>0:
            for index in range(0,len(r["data"])):
                cmnt_id = r["data"]["index"]["id"]
                cmnt_text = r["data"][index]["text"]
                blob = TextBlob(cmnt_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    print"Negative comment : %s" % cmnt_text
                    print"Negative comment found: %s" % cmnt_text
                    r = requests.delete("%smedia/%s/comments/%s/?access_token=%s" % (BASE_URL, media_id, cmnt_id, APP_ACCESS_TOKEN)).json()
                    if r['meta']['code'] == 200:
                        print"Comment successfully deleted!"
                        print"Comment is deleted successfully!"
                    else:
                        print 'Could not delete the comment'

                else:
                    print cmnt_text + 'is a positive comment'
                    print cmnt_text + ' is a positive comment'
        else:
            print" no comments found"
    else:
        print "Error"

#deleting the comment which have negative influence

def start_bot():
    show_menu = True
    while show_menu:
        query = input("What do you want to do? \n 1. Get Owner info. \n 2. Get Owner posts. \n 3. Get user info. \n 4. Get user post \n 5. Liking a post \n 6.Commenting on a post \n 7. Delete comment \n 0. Exit.")
        if query==1:
            owner_info()
        elif query==2:
            owner_post()
        elif query==3:
            username = raw_input("What is the username of that user? ")
            user_info(username)
        elif query==4:
            username = raw_input("What is the username of that user? ")
            user_info(username)
        elif query==5:
            username = raw_input("What is the username of that user? ")
            like_post(username)
        elif query==6:
            username = raw_input("What is the username of that user? ")
            comment_post(username)
        elif query==7:
            username = raw_input("What is the username of that user? ")
            del_comment(username)
        elif query==0:
            show_menu=False
        else:
            print "error"

start_bot()