# YouTube-Downloader
A python application used for downloading YouTube playlists and videos.

# How to use ?
1- Open a terminal window<br />
2- Program arguments:<br />
  . Download type:<br />
    * "-p": for a playlist<br />
    * "-v": for a video<br />
  . Playlist / video URL<br />
  . In case of downloading a playlist, the next two arguments should be two integers:<br />
    * The first integer is the index of the first video in the playlist (the videos are 1-indexed)<br />
    * The second integer is the index of the last video in the playlist (enter -1 if you want to stop at the last video in the playlist)<br />
  . Download path directory type:<br />
    * "-c": download the playlist / video in the current working directory<br />
    * "-r": download the playlist / video using a relative path (provided in the next argument)<br />
    * "-a": download the playlist / video using an absolute path (provided in the next argument)<br />
  . Download path directory: The path of the directory that you want to download the videos to (if you choose "-c" in the previous argument then leave this field empty)<br />
