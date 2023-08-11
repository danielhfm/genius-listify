# genius-listify
A simple python script to convert Spotify Playlists to Genius Lists

Format of the Songs:
Artist – „Song“ [Genius-Indicator]
Whereas the indicators will show, if the song has complete lyrics, is a shellpage, has no lyrics at all or doesn't exist on Genius.	

Before using the script, you will need to get a Genius API Token.
 You can get one here: https://genius.com/api-clients/new

Furthermore you will need a Spotify API Token.
https://developer.spotify.com/documentation/web-api

Create an app over at https://developer.spotify.com/dashboard
Get your Client ID and Client Secret

Add the Genius Token, Spotify Client ID and Spotify Client Secret to your userdata.json file.

Next, you will need to add your Spotify Playlist ID to the userdata.json file.

In order to do that, find your playlist on Spotify, click on the three dots and select "Share" and then "Copy URL".
You will get a link like this: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=65741838282e4a40

The part between "playlist/" and "?si=" is your Playlist ID. In this case: 37i9dQZF1DXcBWIGoYBM5M

Add this ID to your userdata.json file.

Now you can run the script. It will create a file called "tracklist.txt" in the same directory as the script.

You can now copy the contents of this file and paste it into the Genius List Editor.

If you want to use the script again, you should make sure you space out the text in the tracklist.txt file, so new songs will be seperated from the old ones.


