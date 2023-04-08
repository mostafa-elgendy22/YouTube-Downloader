# YouTube-Downloader

A python application used for downloading YouTube playlists and videos.


## Program arguments:

<ol>
    <li>Download type:
        <ul>
            <li>-p: for a playlist</li>
            <li>-v: for a video</li>
        </ul>
    </li>
    <li>Playlist / video URL</li>
    <li>In case of downloading a playlist, the next two arguments should be two integers:
        <ul>
            <li>The first integer is the index of the first video in the playlist (the videos are 1-indexed)</li>
            <li>The second integer is the index of the last video in the playlist (enter -1 if you want to stop at the last video in the playlist)</li>
        </ul>
    </li>
    <li>Download path directory type:
        <ul>
            <li>-c: download the playlist / video in the current working directory</li>
            <li>-r: download the playlist / video using a relative path (provided in the next argument)</li>
            <li>-a: download the playlist / video using an absolute path (provided in the next argument)</li>
        </ul>
    </li>
    <li>Download path directory: The path of the directory that you want to download the videos to (if you choose "-c" in the previous argument then leave this field empty)
    </li>
</ol>

## Example commands:

Download a full playlist:

`python youtube_downloader.py -p "https://www.youtube.com/playlist?list=PL2jrku-ebl3H50FiEPr4erSJiJHURM9BX" 1 -1 -r "..\..\Courses\Cryptography"`

<br>

Download a video:

`python youtube_downloader.py -v "https://www.youtube.com/watch?v=2aHkqB2-46k&list=PL2jrku-ebl3H50FiEPr4erSJiJHURM9BX&index=1" -r "..\..\Courses\Cryptography"`