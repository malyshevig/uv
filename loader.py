from pytube import YouTube
from pytube import Playlist
import os, sys
import logging

logging.basicConfig(stream=sys.stdout, encoding='utf-8', format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)


# url= "https://www.youtube.com/watch?v=HytWgel76rY&list=PLEwK9wdS5g0oZwFwoQT-BrjmkazJWXxfe"
# ir= "c:\\data\\video\\youtube"


class Task:
    def __init__(self, id, link, msg, target):
        self.id = id
        self.link = link
        self.target = target
        self.msg = msg


def is_playlist(link) -> bool:
    return link is not None and link.find("playlist?") >= 0


def download_playlist(link, dest_dir) -> str:
    playlist = Playlist(link)
    logging.info(f"download playlist {playlist.title}")

    new_dir = os.path.join(dest_dir, playlist.title)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    for video in playlist.videos:
        logging.info('downloading : {} with url : {}'.format(video.title, video.watch_url))
        download_video(v=video, dest_dir=new_dir)

    return "ok"

import traceback as tb

def download_video(v, dest_dir) -> str:
    try:
        logging.info(f"get_highest resolution {v}")
        v = v.streams.get_highest_resolution()
        logging.info(f"{v}")
        print(f"{dest_dir}")

        v.download(output_path=dest_dir)
    except BaseException as ex:
        logging.error(f"An error has occurred {ex}", stack_info=True)
        tb.print_exception(ex)
        return "An error has occurred"

    r = "Download is completed successfully"
    return r


def download_link(link, dest_dir) -> str:
    youtube_object = YouTube(url=link)
    return download_video(youtube_object, dest_dir)


def Download(link, dest_dir) -> str:
    if is_playlist(link):
        return download_playlist(link, dest_dir)
    else:
        return download_link(link, dest_dir)
