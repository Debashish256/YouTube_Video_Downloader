import yt_dlp
import os
from threading import Thread

downloads_folder = 'downloads/'  # Folder for server downloads

class DownloadStatus:
    def __init__(self):
        self.status = {
            'percentage': '0%',
            'speed': '0 KiB/s',
            'eta': 'N/A'
        }

    def hook(self, d):
        if d['status'] == 'downloading':
            self.status['percentage'] = d['_percent_str']
            self.status['speed'] = d['_speed_str']
            self.status['eta'] = d['_eta_str']
        elif d['status'] == 'finished':
            self.status['percentage'] = '100%'
            self.status['speed'] = 'N/A'
            self.status['eta'] = 'Completed'

def download_video(video_url):
    status = DownloadStatus()

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
        'progress_hooks': [status.hook],
        'noplaylist': True  # Ensure only the video is downloaded, not the entire playlist
    }

    def download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    thread = Thread(target=download)
    thread.start()

    return status
