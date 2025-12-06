import sys
import signal
import os.path
import subprocess
from urllib.error import URLError
from pytubefix import Playlist
from pytubefix import YouTube
from pytubefix import exceptions
from pytubefix.cli import on_progress


def SIGINT_handler(sig, frame):
    print('\nThe application is interrupted.\n')
    sys.exit(0)
    

def download_file(stream, download_path, file_name, i, end_index, title):
    if stream.filesize >= (2 ** 30): 
        file_size = float("{:.2f}".format(stream.filesize / (2 ** 30)))
        size_unit = "GB"
    else:
        file_size = float("{:.2f}".format(stream.filesize / (2 ** 20)))
        size_unit = "MB"

    if stream.resolution is None:
        stream.resolution = "AUDIO"
    if i is not None:
        print(f"\nDownloading {i} of {end_index}: '{title}' ({file_size} {size_unit}) [{stream.resolution}]")
    else:
        print(f"\nDownloading: '{title}' ({file_size} {size_unit}) [{stream.resolution}]")

    stream.download(download_path, filename = file_name) 
    print("\nSuccessful download.")
    


def download_video(video_URL, download_path, i = None, end_index = None):
    try:
        video = YouTube(video_URL, on_progress_callback=on_progress)
        video.title = video.title.replace("/", "").replace(":", "").replace("?", "").replace("*", "").replace("<", "").replace(">", "").replace("|", "").replace("\\", "").replace("\"", "")
        video.title = f"({i}) {video.title}" if i is not None else video.title
        video_stream = video.streams.filter(adaptive=True).filter(adaptive=True, only_video=True, file_extension='mp4').order_by('resolution').desc().first()
        audio_stream = video.streams.filter(adaptive=True, only_audio=True, file_extension='mp4').order_by('abr').desc().first()
        download_file(video_stream, download_path, video.title + "_video.mp4", i, end_index, video.title)
        download_file(audio_stream, download_path, video.title + "_audio.mp4", i, end_index, video.title)
        return video

    except exceptions.RegexMatchError:
        print("\nInvalid video URL.\n")
        print("\nThis thread might solve your problem: https://stackoverflow.com/questions/70776558/pytube-exceptions-regexmatcherror-init-could-not-find-match-for-w-w .\n")
        sys.exit(0)
    except (URLError, ConnectionResetError):
        print("\nConnection error.\n")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")


def ffmpeg_merge(video, download_path):
    print("\nMerging video and audio...")
    if not download_path:
        download_path = ""
    video_path = download_path + video.title
    subprocess.run([
        "ffmpeg", "-i", video_path + "_video.mp4", "-i", video_path + "_audio.mp4",
        "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", video_path + ".mp4"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    os.remove(video_path + f"_video.mp4")
    os.remove(video_path + f"_audio.mp4")
    print("\nSuccessful merge.")


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
                video = download_video(video_URLs[i - 1], download_path, i, end_index)
                ffmpeg_merge(video, download_path)
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
        video = download_video(video_URL, download_path)
        ffmpeg_merge(video, download_path)
        print("\n")


signal.signal(signal.SIGINT, SIGINT_handler)
main()