# YouTube-Downloader
A python application used for downloading YouTube playlists and videos.

# How to use ?
1- Open a terminal window<br /><br />
2- Program arguments:<br />
&nbsp;&nbsp;&nbsp;. Download type:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* "-p": for a playlist<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* "-v": for a video<br /><br />
&nbsp;&nbsp;&nbsp;. Playlist / video URL<br /><br />
&nbsp;&nbsp;&nbsp;. In case of downloading a playlist, the next two arguments should be two integers:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* The first integer is the index of the first video in the playlist (the videos are 1-indexed)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* The second integer is the index of the last video in the playlist (enter -1 if you want to stop at the last video in the playlist)<br /><br />
&nbsp;&nbsp;&nbsp;. Download path directory type:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* "-c": download the playlist / video in the current working directory<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* "-r": download the playlist / video using a relative path (provided in the next argument)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* "-a": download the playlist / video using an absolute path (provided in the next argument)<br /><br />
&nbsp;&nbsp;&nbsp;. Download path directory: The path of the directory that you want to download the videos to (if you choose "-c" in the previous argument then leave this field empty)<br />

# Example commands:
.\ytd.exe -p https://www.youtube.com/playlist?list=PL2jrku-ebl3H50FiEPr4erSJiJHURM9BX 1 -1 -r "..\..\Courses\Cryptography"&nbsp;&nbsp;(Download the full playlist)<br /><br />
.\ytd.exe -v https://www.youtube.com/watch?v=2aHkqB2-46k&list=PL2jrku-ebl3H50FiEPr4erSJiJHURM9BX&index=1 -r "..\..\Courses\Cryptography"&nbsp;&nbsp;(Download the video)<br />
