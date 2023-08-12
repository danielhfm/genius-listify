# genius-listify
A simple python script to convert Spotify Playlists to Genius Lists

Format of the Songs:
Artist – „Song“ [Genius-Indicator]
Whereas the indicators will show, if the song has complete lyrics, is a shellpage, has no lyrics at all or doesn't exist on Genius.	

# Setup
Before using the script, you will need to put your data into userdata.json.

1. Create a Genius API Client over [here](https://genius.com/api-clients/new)
2. Copy the Access Token and insert it into your userdata.json under genius > "access_token": "ACCESS_TOKEN HERE"
3. Create a Spotify API App over at the [Spotify dashboard](https://developer.spotify.com/dashboard)
4. Go to the settings of your newly created Spotify API App and click "View client secret"
5. Copy the Client ID and insert it into your userdata.json under spotify > "client_id": "CLIENT_ID HERE"
6. Copy the Client secret and insert it into your userdata.json under spotify > "client_secret": "CLIENT_SECRET HERE"
7. Find your desired Spotify Playlist
8. Rightclick the Playlist and select "Share" and then "Copy URL"
9. Fetch the Playlist ID from the link, which is the part between "playlist/" and "?si=" is your Playlist ID.

Example for a Spotify Playlist and how to tell what's the ID:
You will get a link like this: https://open.spotify.com/playlist/<b>37i9dQZF1DXcBWIGoYBM5M</b>?si=65741838282e4a40
In this case: 37i9dQZF1DXcBWIGoYBM5M

Next, you will need to add your Spotify Playlist ID to the userdata.json file.

In order to do that, find your playlist on Spotify, click on the three dots and select "Share" and then "Copy URL".
You will get a link like this: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=65741838282e4a40

The part between "playlist/" and "?si=" is your Playlist ID. In this case: 37i9dQZF1DXcBWIGoYBM5M

After successfully adding the Genius API Token, your Spotify Client ID and Secret and a Playlist ID the script should be working properly.

You can now copy the contents of this file and paste it into your Genius annotation.

If you want to use the script again, you should make sure you space out the text in the tracklist.txt file, so new songs will be seperated from the old ones.


