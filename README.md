# genius-listify
A simple python script to convert Spotify Playlists to Genius Lists

Format of the Songs:
Artist – „Song“ [Genius-Indicator]
Whereas the indicators will show, if the song has complete lyrics, is a shellpage, has no lyrics at all or doesn't exist on Genius.	

# Setup
Before using the script, you will need to put your data into the userdata.json.

1. Create a Genius API Client over [here](https://genius.com/api-clients/new)
2. Copy the Access Token and insert it into your userdata.json under genius > "access_token": "ACCESS_TOKEN HERE"
3. Create a Spotify API App over at the [Spotify dashboard](https://developer.spotify.com/dashboard)
4. Go to the settings of your newly created Spotify API App and click "View client secret"
5. Copy the Client ID and insert it into your userdata.json under spotify > "client_id": "CLIENT_ID HERE"
6. Copy the Client secret and insert it into your userdata.json under spotify > "client_secret": "CLIENT_SECRET HERE"
7. Find your desired Spotify Playlist
8. Rightclick the Playlist and select "Share" and then "Copy URL"
9. Fetch the Playlist ID from the link, which is the part between "playlist/" and "?si=" is your Playlist ID.
10. Copy the Playlist ID and insert it into your userdata.json under spotify > "playlist_id": "YOUR_PLAYLIST_ID HERE"

# How to get the Spotify Playlist ID
Example for a Spotify Playlist and how to tell what's the ID:
You will get a link like this: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=65741838282e4a40
https://open.spotify.com/playlist/<b>37i9dQZF1DXcBWIGoYBM5M</b>?si=65741838282e4a40
Our ID in this case is: 37i9dQZF1DXcBWIGoYBM5M

# Further use of the script
- After running the script it should take a few minutes until the songs are done fetching and your tracklist.txt will open with the fetched songs
- If you're going to use the script a second time it will update the status of all current songs that are still in the spotify playlists and in the tracklist.txt
- If you want to avoid duplicates, you should NEVER delete anything from the tracklist.txt
- If a song shows up twice regardless, it might be because some data like the artists or the name has been changed slightly. In this case delete the one that is further up to avoid duplicates.
- Upon running the script a second time with a new playlist or with the updated playlist you should add a new line at the bottom of the .txt so you can tell the new one and the old one apart better.
