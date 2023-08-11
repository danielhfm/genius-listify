# genius-listify
A simple python script to convert Spotify Playlists to Genius Lists

Format of the Songs:
Artist – „Song“ [Genius-Indicator]
Whereas the indicators will show, if the song has complete lyrics, is a shellpage, has no lyrics at all or doesn't exist on Genius.	

# Setup
Before using the script, you will need to put your data into userdata.json.

Genius API Token can be aquired [here](https://genius.com/api-clients/new)
In order to get a Spotify API Token you will have to create an app over at the [Spotify dashboard](https://developer.spotify.com/dashboard)

Next, you will need to add your Spotify Playlist ID to the userdata.json file.

In order to do that, find your playlist on Spotify, click on the three dots and select "Share" and then "Copy URL".
You will get a link like this: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=65741838282e4a40

The part between "playlist/" and "?si=" is your Playlist ID. In this case: 37i9dQZF1DXcBWIGoYBM5M

After successfully adding the Genius API Token, your Spotify Client ID and Secret and a Playlist ID the script should be working properly.

You can now copy the contents of this file and paste it into your Genius annotation.

If you want to use the script again, you should make sure you space out the text in the tracklist.txt file, so new songs will be seperated from the old ones.


