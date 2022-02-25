import sys
import os.path
from pytube import Playlist
from pytube import YouTube
from pytube.cli import on_progress


def download_video(video_URL, download_path):
    try:
        video = YouTube(video_URL, on_progress_callback = on_progress)
        stream = video.streams.filter(progressive = True, file_extension = "mp4").last()
        if stream.filesize >= (2 ** 30): 
            file_size = float("{:.2f}".format(stream.filesize / (2 ** 30)))
            size_unit = "GB"
        else:
            file_size = float("{:.2f}".format(stream.filesize / (2 ** 20)))
            size_unit = "MB"
        if sys.argv[1] == "-p":
            print("\nDownloading " + str(i) + " of " + str(end_index) + ": '" + video.title + "' (" + str(file_size) + " " + size_unit + ")" + " [" + stream.resolution + "]")
        else:
            print("\nDownloading: '" + video.title + "' (" + str(file_size) + " " + size_unit + ")" + " [" + stream.resolution + "]")
        if download_path is None:
            stream.download()
        else:
            stream.download(download_path)
        print("\nSuccessful download.")

    except:
        print("\nSomething went wrong.\n")
        quit()


def create_download_path(type, path):
    if type == "-r":
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        download_path = os.path.join(file_dir, path)
    elif type == "-a":
        download_path = path
    else:
        download_path = None 
    return download_path


try:
    if sys.argv[1] == "-p":
        if (len(sys.argv) != 7 and sys.argv[5] != "-c") or (len(sys.argv) != 6 and sys.argv[5] == "-c"):
            quit()
        playlist_URL = sys.argv[2]
        start_index = int(sys.argv[3])
        end_index = int(sys.argv[4])
        download_path_type = sys.argv[5]
        if download_path_type != "-a" and download_path_type != "-r" and download_path_type != "-c":
            quit()
        download_path = create_download_path(download_path_type, sys.argv[6] if len(sys.argv) == 7 else None)

    elif sys.argv[1] == "-v":
        if (len(sys.argv) != 5 and sys.argv[3] != "-c") or (len(sys.argv) != 4 and sys.argv[3] == "-c"):
            quit()
        video_URL = sys.argv[2]
        download_path_type = sys.argv[3]
        if download_path_type != "-a" and download_path_type != "-r" and download_path_type != "-c":
            quit()
        download_path = create_download_path(download_path_type, sys.argv[4] if len(sys.argv) == 5 else None)
    
    else:
        quit()

except:
    print("\nInvalid arguments.\n")
    quit()


if sys.argv[1] == "-p":
    print("\nYoutube Playlist Downloader")
    playlist = Playlist(playlist_URL)
    if end_index == -1:
        end_index = len(playlist.videos)
    if start_index <= 0 or start_index > len(playlist.videos):
        print("\nInvalid value for start index.\n")
        quit()
    if end_index <= 0 or end_index > len(playlist.videos):
        print("\nInvalid value for end index.\n")
        quit()
    if start_index > end_index:
        print("\nInvalid value for start index, start index shouldn't be greater than end index.\n")
        quit()
    video_URLs = playlist.video_urls
    print("\nPlease wait...")
    for i in range(start_index, end_index + 1):
        download_video(video_URLs[i - 1], download_path)
    print("\nThe playlist was downloaded successfully.\n")

else: 
    print("\nYoutube Downloader")
    print("\nPlease wait...")
    download_video(video_URL, download_path)
    print("\n")