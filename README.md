# YouTube-Downloader
A python application used for downloading YouTube playlists and videos.

# How to use ?
1- Open a terminal window__
2- Program arguments:
  . Download type:
    * "-p": for a playlist
    * "-v": for a video
  . Playlist / video URL
  . In case of downloading a playlist, the next two arguments should be two integers:
    * The first integer is the index of the first video in the playlist (the videos are 1-indexed)
    * The second integer is the index of the last video in the playlist (enter -1 if you want to stop at the last video in the playlist)
  . Download path directory type: 
    * "-c": download the playlist / video in the current working directory
    * "-r": download the playlist / video using a relative path (provided in the next argument)
    * "-a": download the playlist / video using an absolute path (provided in the next argument)
  . Download path directory: The path of the directory that you want to download the videos to (if you choose "-c" in the previous argument then leave this field empty)
