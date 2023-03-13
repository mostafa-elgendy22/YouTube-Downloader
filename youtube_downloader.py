from multiprocessing.sharedctypes import Value
import sys
import signal
import os.path
from urllib.error import URLError
from pytube import Playlist
from pytube import YouTube
from pytube import exceptions
from pytube.cli import on_progress

def SIGINT_handler(sig, frame):
    print('\nThe application is interrupted.\n')
    sys.exit(0)

def download_video(video_URL, download_path, i = None, end_index = None, resolution = None):
    try:
        video = YouTube(video_URL, on_progress_callback = on_progress)
        if sys.argv[1] == "-v":
            resolution = select_resolution(video.streams.filter(progressive = True), video.title)
        stream = video.streams.filter(progressive = True, file_extension = "mp4").get_by_resolution(resolution)
        if stream.filesize >= (2 ** 30): 
            file_size = float("{:.2f}".format(stream.filesize / (2 ** 30)))
            size_unit = "GB"
        else:
            file_size = float("{:.2f}".format(stream.filesize / (2 ** 20)))
            size_unit = "MB"

        if sys.argv[1] == "-p":
            print(f"\nDownloading {i} of {end_index}: '{video.title}' ({file_size} {size_unit}) [{stream.resolution}]")
        else:
            print(f"\nDownloading: '{video.title}' ({file_size} {size_unit}) [{stream.resolution}]")

        stream.download(download_path) 
        print("\nSuccessful download.")

    except exceptions.RegexMatchError:
        print("\nInvalid video URL.\n")
        print("\nThis thread might solve your problem: https://stackoverflow.com/questions/70776558/pytube-exceptions-regexmatcherror-init-could-not-find-match-for-w-w .\n")
        sys.exit(0)
    
    except (URLError, ConnectionResetError):
        print("\nConnection error.\n")
        sys.exit(0)

def select_resolution(streams, title):
    resolutions = []
    for stream in streams:
        if stream.mime_type == "video/mp4" and stream.resolution not in resolutions:
            resolutions.append(stream.resolution)
    print(f"\nAvailable resolutions for '{title}':")
    for i in range(len(resolutions)):
        print(f"{i + 1}. {resolutions[i]}")
    choice = int(input(f"Choose a resolution: "))
    return resolutions[choice - 1]

def find_resolutions(video_URLs):
    resolutions = {}
    for video_URL in video_URLs:
        video = YouTube(video_URL)
        for stream in video.streams.filter(progressive = True):
            if stream.mime_type == "video/mp4" and stream.resolution not in resolutions:
                resolutions[stream.resolution] = 1
            elif stream.mime_type == "video/mp4" and stream.resolution in resolutions:
                resolutions[stream.resolution] += 1
        
    # remove resolutions that are not available in all videos
    for resolution in list(resolutions):
        if resolutions[resolution] != len(video_URLs):
            del resolutions[resolution]
    return list(resolutions)


def create_download_path(type, path):
    if type == "-r":
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        download_path = os.path.join(file_dir, path)
    elif type == "-a":
        download_path = path
    else:
        download_path = None 
    return download_path

def main():
    try:
        if sys.argv[1] == "-p":
            if (len(sys.argv) != 7 and sys.argv[5] != "-c") or (len(sys.argv) != 6 and sys.argv[5] == "-c"):
                raise ValueError
            playlist_URL = sys.argv[2]
            start_index = int(sys.argv[3])
            end_index = int(sys.argv[4])
            download_path_type = sys.argv[5]
            if download_path_type != "-a" and download_path_type != "-r" and download_path_type != "-c":
                raise ValueError
            download_path = create_download_path(download_path_type, sys.argv[6] if len(sys.argv) == 7 else None)

        elif sys.argv[1] == "-v":
            if (len(sys.argv) != 5 and sys.argv[3] != "-c") or (len(sys.argv) != 4 and sys.argv[3] == "-c"):
                raise ValueError
            video_URL = sys.argv[2]
            download_path_type = sys.argv[3]
            if download_path_type != "-a" and download_path_type != "-r" and download_path_type != "-c":
                raise ValueError
            download_path = create_download_path(download_path_type, sys.argv[4] if len(sys.argv) == 5 else None)
        
        else:
            raise ValueError

    except (IndexError, ValueError):
        print("\nInvalid arguments.\n")
        sys.exit(0)


    if sys.argv[1] == "-p":
        print("\nYoutube Playlist Downloader")
        try:
            if not("playlist" in playlist_URL):
                raise ValueError
            playlist = Playlist(playlist_URL)
            
            video_URLs = playlist.video_urls
            if playlist.length == 0:
                raise ValueError

            if end_index == -1:
                end_index = len(playlist.videos)
            if start_index <= 0 or start_index > len(playlist.videos):
                print("\nInvalid value for start index.\n")
                sys.exit(0)
            if end_index <= 0 or end_index > len(playlist.videos):
                print("\nInvalid value for end index.\n")
                sys.exit(0)
            if start_index > end_index:
                print("\nInvalid value for start index, start index shouldn't be greater than end index.\n")
                sys.exit(0)
            print("\nPlease wait...")
            video_URLs = video_URLs[start_index - 1:end_index]
            
            resolutions = find_resolutions(video_URLs)
            print(f"\nAvailable resolutions for the playlist:")
            for i in range(len(resolutions)):
                print(f"{i + 1}. {resolutions[i]}")
            
            choice = int(input(f"Choose a resolution: "))
            resolution = resolutions[choice - 1]
            
            for i in range(len(video_URLs)):
                download_video(video_URLs[i], download_path, start_index + i, end_index, resolution)
            print("\nThe playlist was downloaded successfully.\n")

        except (ValueError, KeyError):
            print("\nInvalid playlist URL.\n")
            sys.exit(0)
        
        except URLError:
            print("\nConnection error.\n")
            sys.exit(0)

    else: 
        print("\nYoutube Downloader")
        print("\nPlease wait...")
        download_video(video_URL, download_path)
        print("\n")


signal.signal(signal.SIGINT, SIGINT_handler)
main()
