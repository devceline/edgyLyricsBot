"""
Edgy Lyric Bot
"""
import json
from datetime import datetime
from math import floor
from random import random, seed
from apscheduler.schedulers.blocking import BlockingScheduler
from api_controller.genius_client import GeniusClient
from tweet import tweet, direct_message

def calculate_edge(referent):
    """
    Calculates edge based on annotations and text
    """

    score = 0

    text = referent["fragment"]
    edge_multiplier = 1

    with open("config.json") as config:
        edgy_words = json.load(config)["edge"]["words"]

    annotations = []
    for annotation in referent["annotations"]:
        for child in annotation["body"]["dom"]["children"]:
            if isinstance(child, str):
                annotations.append(child)

    for word, value in edgy_words.items():
        if word in text.lower():
            score += value

        for annotation in annotations:
            if word in annotation.lower():
                edge_multiplier += (value/30)


    return score * edge_multiplier

def max_fragment_edge(referents):
    """
    Attempts to get the absolute edgiest fragment of a song
    """
    max_score_referent = referents[floor(random() * 10 % len(referents))]["fragment"]
    max_score = 1

    for referent in referents:
        score = calculate_edge(referent)
        if score > max_score:
            max_score = score
            max_score_referent = referent["fragment"]

    return [max_score_referent, floor(max_score)]

def get_edgy_fragment(genius_client, artist_name):
    """
    Attempts to get an edgy fragment from a random song
    """
    song_id = genius_client.get_artist_top_song_id(artist_name)
    how_old = floor((int(datetime.now().year) - int(genius_client.get_song(song_id)["release_date"][0:4]))/5)

    song_referents = genius_client.get_song_referents(song_id)

    if len(song_referents) == 0:
        return get_edgy_fragment(genius_client, artist_name)

    edgiest_fragment = max_fragment_edge(song_referents)
    edgiest_fragment[1] *= how_old if how_old > 0 else 1

    return edgiest_fragment

def begin_schedule():
    """
    Starts a scheduler
    """
    print("Online - start")
    scheduler = BlockingScheduler()
    with open("config.json") as config:
        interval = json.load(config)["edge"]["interval"]

    scheduler.add_job(main, 'interval', hours=interval)
    direct_message("I am online!!!")
    scheduler.start()

def main(begin=False):
    """
    Main function
    """
    print(begin)
    print("Started..")
    genius = GeniusClient()
    seed(datetime.now())
    with open("config.json") as config:
        artists = json.load(config)["edge"]["artists"]

    artist_name = artists[floor((random() * 10) % len(artists))]
    print(f"Checking for {artist_name}")

    edgiest_fragment = get_edgy_fragment(genius, artist_name)

    if edgiest_fragment[0] == "Failed":
        direct_message("mmaAAAMMMAAAAAAA")
        direct_message(f"""Failed:
                       \ngetting edgy song for band: {artist_name} 
                       \nNo edgy songs found""")
        return

    message = f'{edgiest_fragment[0]}'
    append = f'\n-{artist_name}\nscore:{edgiest_fragment[1]}'
    required_len = 280 - len(append) - 3

    while len(message) > required_len:
        message = message[0:-1]

    if len(message) == required_len:
        message += "..."

    message += append

    try:
        tweet(message)
    except Exception as err:
        direct_message(str(err))

    if begin:
        begin_schedule()
