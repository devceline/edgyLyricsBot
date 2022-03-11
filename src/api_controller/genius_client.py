import requests
from datetime import datetime
import json
from random import random, seed
from math import floor

class GeniusClient:

    class decorators:
        def jsonify(func):
            def jsonify_wrapper(*args, **kwargs):
                func_rs = func(*args, **kwargs)
                json_rs = func_rs[0].json()

                if json_rs["meta"]["status"] != 200:
                    raise Exception("Error in request", json_rs["meta"])

                return json_rs["response"][func_rs[1]]
            return jsonify_wrapper

        def authenticate(func):
            def authentication_wrapper(*args, **kwargs):
                if(func(*args, **kwargs)[0].status_code == 401):
                    self = args[0]
                    self.authToken = self.getAuthToken()
                    kwargs["token"] = self.authToken
                    return func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            return authentication_wrapper


    def __init__(self):
        self.base_url = "https://api.genius.com"

    def getAuthToken(self):
        url = f'{self.base_url}/oauth/token'

        clientId = ""
        clientSecret = ""
        with open("config.json") as f:
            jsonInfo = json.load(f)["genius"]
            clientId = jsonInfo["clientId"]
            clientSecret = jsonInfo["clientSecret"]

        authToken = requests.post(url, data = {
            "client_id": clientId,
            "client_secret": clientSecret,
            "grant_type": "client_credentials"
        })

        rs = authToken.json()
        return f"bearer {rs['access_token']}"


    @decorators.jsonify
    @decorators.authenticate
    def search(self, searchTerm, token=""):
        url = f'{self.base_url}/search?q={searchTerm}'
        searchRs = requests.get(url, headers = {"Authorization": token})
        return [searchRs, "hits"]

    @decorators.jsonify
    @decorators.authenticate
    def get_song(self, song_id, token=""):
        url = f'{self.base_url}/songs/{song_id}'
        songRs = requests.get(url, headers = {"Authorization": token})
        return [songRs, "song"]

    @decorators.jsonify
    @decorators.authenticate
    def get_artist_songs(self, artist_name, token=""):
        search_result = self.search(artist_name)
        artist_id = search_result[0]["result"]["primary_artist"]["id"]
        url = f'{self.base_url}/artists/{artist_id}/songs'
        songsRs = requests.get(url, headers = {"Authorization": token})
        return [songsRs, "songs"]

    @decorators.jsonify
    @decorators.authenticate
    def get_song_referents(self, song_id, token=""):

        if(song_id == None):
            raise Exception("Referents", "Song ID is null")

        url = f'{self.base_url}/referents?song_id={song_id}'
        referentsRs = requests.get(url, headers = {"Authorization": token})
        return [referentsRs, "referents"]

    def get_artist_top_song_id(self, artist_name):
        seed(datetime.now())
        songs = self.get_artist_songs(artist_name)
        song_id = floor((random() * 10) % len(songs))
        song_id = songs[song_id]["id"]
        return song_id

    def get_song_fragments(self, song_id):
        if(song_id == None):
            raise Exception("Fragments", "Song ID is null")

        referents = self.get_song_referents(song_id)
        fragments = []

        for referent in referents:
            fragments.append(referent["fragment"])

        return fragments
