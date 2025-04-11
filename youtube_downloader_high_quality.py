import sys
import signal
import os.path
from urllib.error import URLError
from pytubefix import Playlist
from pytubefix import YouTube
from pytubefix import exceptions
from pytubefix.cli import on_progress
import subprocess


def SIGINT_handler(sig, frame):
    print('\nThe application is interrupted.\n')
    sys.exit(0)
    

def download_video(video_URL, download_path, i = None, end_index = None):
    try:
        video = YouTube(video_URL, on_progress_callback=on_progress, use_oauth=True, allow_oauth_cache=True)
        video_stream = video.streams.filter(adaptive=True).filter(mime_type='video/webm').first()

        if video_stream.filesize >= (2 ** 30): 
            file_size = float("{:.2f}".format(video_stream.filesize / (2 ** 30)))
            size_unit = "GB"
        else:
            file_size = float("{:.2f}".format(video_stream.filesize / (2 ** 20)))
            size_unit = "MB"

        if sys.argv[1] == "-p":
            print(f"\nDownloading {i} of {end_index}: '{video.title}' ({file_size} {size_unit}) [{video_stream.resolution}]")
        else:
            print(f"\nDownloading: '{video.title}' ({file_size} {size_unit}) [{video_stream.resolution}]")

        video_stream.download(download_path) 
        print("\nSuccessful download.")
        
        ##########################################################################################
        audio_stream = video.streams.filter(adaptive=True).filter(mime_type='audio/webm').first()
        if audio_stream.filesize >= (2 ** 30): 
            file_size = float("{:.2f}".format(audio_stream.filesize / (2 ** 30)))
            size_unit = "GB"
        else:
            file_size = float("{:.2f}".format(audio_stream.filesize / (2 ** 20)))
            size_unit = "MB"
        
        if sys.argv[1] == "-p":
            print(f"\nDownloading {i} of {end_index}: '{video.title}' ({file_size} {size_unit}) [{audio_stream.resolution}]")
        else:
            print(f"\nDownloading: '{video.title}' ({file_size} {size_unit}) [AUDIO]")

        audio_stream.download(download_path) 
        print("\nSuccessful download.")

        print("\nMerging video and audio...")
        video.title = video.title.replace("/", "")
        video.title = video.title.replace(":", "")
        video.title = video.title.replace("?", "")
        video.title = video.title.replace("*", "")
        video.title = video.title.replace("<", "")
        video.title = video.title.replace(">", "")
        video.title = video.title.replace("|", "")
        video.title = video.title.replace("\\", "")
        video.title = video.title.replace("\"", "")
        video.title = video.title.replace("'", "")
        if not download_path:
            download_path = ""
        subprocess.run([
            "ffmpeg", "-i", download_path + video.title + ".webm", "-i", download_path + video.title + ".m4a",
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", download_path + video.title + ".mp4",
            "-y"  # Overwrite without asking
        ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        os.remove(download_path + video.title + ".webm")
        os.remove(download_path + video.title + ".m4a")
        print("\nSuccessful merge.")


    except exceptions.RegexMatchError:
        print("\nInvalid video URL.\n")
        print("\nThis thread might solve your problem: https://stackoverflow.com/questions/70776558/pytube-exceptions-regexmatcherror-init-could-not-find-match-for-w-w .\n")
        sys.exit(0)
    
    except (URLError, ConnectionResetError):
        print("\nConnection error.\n")
        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}")


def create_download_path(type, path):
    if type == "-r":
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        download_path = os.path.join(file_dir, path)
    elif type == "-a":
        download_path = path + "\\"
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
            for i in range(start_index, end_index + 1):
                download_video(video_URLs[i - 1], download_path, i, end_index)
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