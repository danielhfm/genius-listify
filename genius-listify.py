import os
import requests
import json
import editdistance
from tqdm import tqdm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Track Class
class Track:
    def __init__(self, artist, title):
        # Spotify specific attributes
        self.artist = artist # Primary artist of the track
        self.all_artists = None # All artists of the track
        self.title = title # Title of the track
        self.song_key = None # Key of the track

        # Genius specific attributes
        self.genius_search_one = None # Search term for Genius
        self.genius_search_two = None # Search term for Genius
        self.song_id = None # ID of the track
        self.url = None # URL of the track on Genius
        self.isShell = False # Indicator for wheter the track has a shellpage or not; default is False
        self.hasLyrics = False # Indicator for whether the track has a complete lyrics page or not; default is False
        self.isVerified = False # Indicator for whether the track has been marked as complete or not; default is False

# API Connections for Spotify and Genius

# Load user data from JSON file
with open("userdata.json") as f:
    userdata = json.load(f)

sp_client_id = userdata["spotify"]["client_id"]
sp_client_secret = userdata["spotify"]["client_secret"]
sp_playlist_id = userdata["spotify"]["playlist_id"]
gns_access_token = userdata["genius"]["access_token"]

# Spotify API
client_credentials_manager = SpotifyClientCredentials(sp_client_id, sp_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

img = sp.playlist_cover_image(sp_playlist_id)
print("Playlist Image: ", img[0]["url"])

# Genius API
gns_search_endpoint = "https://api.genius.com/search"
gns_song_endpoint = "https://api.genius.com/songs/"
gns_headers = {
    "Authorization": f"Bearer {gns_access_token}"
}

# Functions

# Function to fetch all tracks from a playlist on Spotify
# @param playlist_id: The id of the playlist on Spotify
# Returns an array of tracks
def fetch_playlist(playlist_id):
    playlist = sp.playlist(playlist_id)
    tracks = playlist["tracks"]
    return tracks

# Function to filter the important data from the playlist array and return a list of tracks using the Track class
# @param tracks: The array of tracks from the Spotify API
# Returns a list of tracks and the amount of tracks in the playlist
def filter_tracks(tracks):
    tracklist = []
    counter = 0
    for track in tracks["items"]:

        # Check if the track is None
        if track["track"] is None:
            #print(f"Track {counter} is None")
            counter += 1
            continue
        
        # Adjusting Title # - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # Assign the primary artist and title of the track
        title = track["track"]["name"]

        # filter the title for unnecessary stuff
        if " (feat." in title:
            title = title.split(" (feat.")[0]
        if " (ft." in title:
            title = title.split(" (ft.")[0]
        # if " - radio edit" in title:
        #     title = title.replace(" - radio edit", " (radio edit)")
        if " - " in title:
            parts = title.split(" - ")
            title = f"{parts[0].strip()} ({parts[1].strip()})"
            

        # Adjusting Artist properties # - - - - - - - - - - - - - - - - - - - - -

        artist = track["track"]["artists"][0]["name"]

        # fetching all artists of the track
        artists = [artist["name"] for artist in track["track"]["artists"]]
        # making a string out of the artists
        if len(artists) == 1:
            artist_str = artists[0]
        elif len(artists) == 2:
            artist_str = " & ".join(artists)
        else:
            artist_str = ", ".join(artists[:-1]) + " & " + artists[-1]
        
        # Create the object of the current track
        current_track = Track(artist, title)
        current_track.all_artists = artist_str
        current_track.song_key = f"{artist_str} – „{title}“"
        current_track.genius_search_one = f"{artist} {title}"
        current_track.genius_search_two = f"{artist_str} - {title}"
        tracklist.append(current_track)

        counter += 1

    return tracklist, counter

# Function to check two strings for similarity using the Levenshtein distance
# @param string1: The first string to compare
# @param string2: The second string to compare
# Returns True if the Distance is <= 1, else False
def check_strings(string1, string2):
    # remove all special characters from the strings
    string1 = string1.lower()
    string1 = string1.replace("’", "'")
    string1 = string1.replace(" ", "")
    string1 = string1.replace("\u200b", "")

    string2 = string2.lower()
    string2 = string2.replace("’", "'")
    string2 = string2.replace(" ", "")
    string2 = string2.replace("\u200b", "")

    # Compute the Levenshtein distance between the titles
    distance = editdistance.eval(string1, string2)

    if distance <= 1:
        return True
    else:
        #print(f"Distance between {string1} and {string2} is {distance}")
        return False



# Function to search for the track on Genius
def search_track(track, search_string):
    search_params = {"q": search_string}
    response = requests.get(gns_search_endpoint, params=search_params, headers=gns_headers)
    response.raise_for_status()
    response_data = response.json()

    # if search string = Bosca & Celo & Abdi - Teer, give out all data please
    if search_string == "Bosca & Celo & Abdi - Teer":
        print(response_data)
        

    # Check if the track was found
    if response_data["meta"]["status"] == 200 and len(response_data["response"]["hits"]) != 0:
        if check_strings(track.title, response_data["response"]["hits"][0]["result"]["title"]):
            track.song_id = response_data["response"]["hits"][0]["result"]["id"]
            track.url = response_data["response"]["hits"][0]["result"]["url"]
        else:
            # check the second result if the first one is not correct
            if len(response_data["response"]["hits"]) > 1:
                if check_strings(track.title, response_data["response"]["hits"][1]["result"]["title"]):
                    track.song_id = response_data["response"]["hits"][1]["result"]["id"]
                    track.url = response_data["response"]["hits"][1]["result"]["url"]
                else:
                    return False
    
# Function that fetches genius song data for a track using the id
# @param track: The track object
# Returns the track object with the fetched data
def fetch_song_data(track):
    # Fetch the song data from Genius
    response = requests.get(gns_song_endpoint + str(track.song_id), headers=gns_headers)
    response.raise_for_status()
    response_data = response.json()

    # Check if the song was found
    if response_data["meta"]["status"] == 200:
        # check if the song is marked as complete by an editor+ on Genius
        if response_data["response"]["song"]["lyrics_marked_complete_by"] is not None:
            track.isVerified = True
        # check if the song is a shell page
        if response_data["response"]["song"]["lyrics_state"] == "unreleased" or response_data["response"]["song"]["lyrics_state"] == "incomplete":
            track.isShell = True
        # check if the song has lyrics
        if response_data["response"]["song"]["lyrics_state"] == "complete":
            track.hasLyrics = True
    # else:
    #     print(f"Song with id {track.song_id} not found on Genius")

# Function to get the current Status
# @param tracklist: The list of tracks
# Prints the current status of the tracklist
def get_status(tracklist):
    amount_missing = 0
    amount_verified = 0
    amount_shell = 0
    amount_complete = 0
    for track in tracklist:
        if track.song_id is None:
            amount_missing += 1
        else:
            if track.isVerified:
                amount_verified += 1
            if track.isShell:
                amount_shell += 1
            if track.hasLyrics:
                amount_complete += 1
    print("- - - - - Status - - - - -")
    print(f"Total: {len(tracklist)}")            
    print(f"Missing: {amount_missing}")
    print(f"Verified: {amount_verified}")
    print(f"Shell: {amount_shell}")
    print(f"Complete: {amount_complete}")

#**********************************************************************************************************************
# Main Function
#**********************************************************************************************************************

# Fetching the playlist from Spotify
playlist = fetch_playlist(sp_playlist_id)

# filter the spotify playlist to match genius standards
temp = filter_tracks(playlist)

tracklist = temp[0]
amount = temp[1]

# Search for the tracks on Genius
for track in tqdm(tracklist, desc="Searching tracks"):

    if search_track(track, track.genius_search_one) == False:
        search_track(track, track.genius_search_two)

    if track.song_id is not None:
        fetch_song_data(track)

with open("tracklist.txt", "r+", encoding="utf-8") as f:
    lines = f.readlines()

    for track in tqdm(tracklist, desc="Writing to file"):
            # Check if song key is already in the file
            for i, line in enumerate(lines):
                if track.song_key in line:
                    # print(f"{track.song_key} found in file")
                    isChanged = False
                    # Check if the song has a ⛔, if it does, check if it is correct
                    if "⛔" in line:
                        if track.hasLyrics or track.isShell:
                            if track.isVerified:
                                new_line = f"- [{track.song_key}]({track.url}) ✅\n"
                                lines[i] = new_line
                            elif track.isShell:
                                new_line = f"- [{track.song_key}]({track.url}) 🐚\n"
                                lines[i] = new_line
                            elif track.hasLyrics:
                                new_line = f"- [{track.song_key}]({track.url})\n"
                                lines[i] = new_line
                            isChanged = True
                    elif "🐚" in line:
                        if not track.isShell:
                            if track.isVerified:
                                new_line = f"- [{track.song_key}]({track.url}) ✅\n"
                                lines[i] = new_line
                            elif track.hasLyrics:
                                new_line = f"- [{track.song_key}]({track.url})\n"
                                lines[i] = new_line
                            isChanged = True
                    elif "✅" not in line:
                        if track.isVerified:
                            new_line = f"- [{track.song_key}]({track.url}) ✅\n"
                            lines[i] = new_line
                            isChanged = True
                    
                    if isChanged:
                        f.seek(0)
                        f.writelines(lines)
                        f.truncate()
                    break
            else:
                # Add the song to the file
                new_line = ""

                if track.isShell:
                    new_line = f"- [{track.song_key}]({track.url}) 🐚\n"
                if track.hasLyrics:
                    new_line = f"- [{track.song_key}]({track.url})\n"
                if track.isVerified:
                    new_line = f"- [{track.song_key}]({track.url}) ✅\n"
                if not track.isShell and not track.hasLyrics and not track.isVerified:
                    new_line = f"- [{track.song_key}]() ⛔\n"
                
                if new_line != "":
                    lines.append(new_line)
                
                f.seek(0)
                f.writelines(lines)
                f.truncate()              

get_status(tracklist)

# Open the tracklist file in the default application
#("tracklist.txt")






