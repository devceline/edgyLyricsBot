import twitter
import json


def tweet(message):

    APP_KEY = ""
    APP_SECRET = ""
    OAUTH_TOKEN = ""
    OAUTH_TOKEN_SECRET = ""

    with open("config.json") as f:
        json_info = json.load(f)["twitter"]
        APP_KEY = json_info["app_key"]
        APP_SECRET = json_info["app_secret"]
        OAUTH_TOKEN = json_info["oauth_token"]
        OAUTH_TOKEN_SECRET = json_info["oauth_token_secret"]

    api = twitter.Api(access_token_key=OAUTH_TOKEN, access_token_secret=OAUTH_TOKEN_SECRET, consumer_key=APP_KEY, consumer_secret=APP_SECRET)
    print("Tweeting...")
    api.PostUpdate(message)


def direct_message(message):
    APP_KEY = ""
    APP_SECRET = ""
    OAUTH_TOKEN = ""
    OAUTH_TOKEN_SECRET = ""
    TARGET = ""

    with open("config.json") as f:
        json_info = json.load(f)["twitter"]
        APP_KEY = json_info["app_key"]
        APP_SECRET = json_info["app_secret"]
        OAUTH_TOKEN = json_info["oauth_token"]
        OAUTH_TOKEN_SECRET = json_info["oauth_token_secret"]
        TARGET = json_info["mention"]
        

    api = twitter.Api(access_token_key=OAUTH_TOKEN, access_token_secret=OAUTH_TOKEN_SECRET, consumer_key=APP_KEY, consumer_secret=APP_SECRET)

    api.PostDirectMessage(message, screen_name=TARGET, return_json=True)


    




