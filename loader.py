from pytube import YouTube
from pytube import Playlist
import os, sys
import logging

logging.basicConfig(stream=sys.stdout,encoding='utf-8', format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

url= "https://www.youtube.com/watch?v=HytWgel76rY&list=PLEwK9wdS5g0oZwFwoQT-BrjmkazJWXxfe"
dir= "c:\\data\\video\\youtube"


class Task:
    def __init__(self, id, link, msg, target=dir):
        self.id = id
        self.link = link
        self.target = target
        self.msg = msg


def is_playlist(link)-> bool:
    return link is not None and link.find("playlist?") >=0


def download_playlist(link) -> str:
    playlist = Playlist(link)
    logging.info(f"download playlist {playlist.title}")


    new_dir = os.path.join(dir,playlist.title)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    for video in playlist.videos:
        print('downloading : {} with url : {}'.format(video.title, video.watch_url))
        download_video(v=video,dest_dir=new_dir)

    return "ok"


def download_video(v, dest_dir=dir) -> str:
    v = v.streams.get_highest_resolution()
    try:
        v.download(output_path=dest_dir)
    except BaseException as ex:
        print(f"An error has occurred {ex}")
        return "An error has occurred"

    r = "Download is completed successfully"
    return r


def download_link(link)->str:
    youtube_object = YouTube(url=link)
    return download_video(youtube_object)


def Download(link)->str:
    if is_playlist(link):
        return download_playlist(link)
    else:
        return download_link(link)



