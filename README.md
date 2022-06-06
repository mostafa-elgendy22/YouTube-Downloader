# YouTube-Downloader
A python application used for downloading YouTube playlists and videos.

# How to use ?
##### Program arguments:
1. Download type:
* "-p": for a playlist
* "-v": for a video
2. Playlist / video URL
3. In case of downloading a playlist, the next two arguments should be two integers:
* The first integer is the index of the first video in the playlist (the videos are 1-indexed) 
* The second integer is the index of the last video in the playlist (enter -1 if you want to stop at the last video in the playlist)  
4. Download path directory type: 
* "-c": download the playlist / video in the current working directory 
* "-r": download the playlist / video using a relative path (provided in the next argument) 
* "-a": download the playlist / video using an absolute path (provided in the next argument)  
5. Download path directory: The path of the directory that you want to download the videos to (if you choose "-c" in the previous argument then leave this field empty) 

# Example commands:
* Download the full playlist <br />
`
python youtube_downloader.py -p "https://www.youtube.com/playlist?list=PL2jrku-ebl3H50FiEPr4erSJiJHURM9BX" 1 -1 -r "..\..\Courses\Cryptography"
`
* Download the video <br />
`  
python youtube_downloader.py -v "https://www.youtube.com/watch?v=2aHkqB2-46k&list=PL2jrku-ebl3H50FiEPr4erSJiJHURM9BX&index=1" -r "..\..\Courses\Cryptography"
`