import os, sys, subprocess, yt_dlp, tkinter
from tkinter import filedialog

def setPath():
    path = filedialog.askdirectory()
    print(f"Download path set to: {path}")
    return path

def checkIfPlaylist(url):
    if 'playlist?list=' in url:
        print("\n\n*******DETECTED PLAYLIST******\n\n")
        return '/%(playlist_title)s'
    return ''

def checkIfAudio(myDict):
    try:
        mediaType = int(input("Enter 1 for Video, Enter 2 for Audio:\t"))
        if mediaType == 2:
            myDict['format'] = 'bestaudio'
            myDict['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
                'preferredquality': '192'
            })
    except ValueError:
        print("Invalid input. Assuming default option: Video")
    return myDict

def checkIfThumbnail(myDict):
    try:
        isThumb = int(input("Enter 1 for thumbnail download, press ENTER to skip:\t"))
        if isThumb == 1:
            myDict['writethumbnail'] = True
            myDict['postprocessors'].append({'key': 'EmbedThumbnail'})
    except ValueError:
        pass
    return myDict

def checkIfSubtitles(myDict):
    try:
        isSubtitle = int(input("Enter 1 for subtitle download, press ENTER to skip:\t"))
        if isSubtitle == 1:
            myDict['writesubtitles'] = True
        isEmbeddedSubtitle = int(input("Enter 1 to embed subtitles into the video, press ENTER to leave as separate file:\t"))
        if isEmbeddedSubtitle == 1:
            myDict['postprocessors'].append({'key': 'FFmpegEmbedSubtitle'})
    except ValueError:
        pass
    return myDict

def checkDownloadQuality(myDict):
    resolution_map = {
        '144': '144p', '144p': '144p',
        '240': '240p', '240p': '240p',
        '360': '360p', '360p': '360p',
        '480': '480p', '480p': '480p',
        '720': '720p', '720p': '720p', 'hd': '720p',
        '1080': '1080p', '1080p': '1080p', 'fhd': '1080p', 'full hd': '1080p',
        '1440': '1440p', '1440p': '1440p', 'qhd': '1440p', 'quad hd': '1440p',
        '2560': '2160p', '2560p': '2160p', 'uhd': '2160p', '4k': '2160p',
    }

    print("\nAvailable Resolutions: 144, 240, 360, 480, 720 (hd), 1080 (fhd/full hd), 1440 (qhd/quad hd), 2560 (uhd/4k)")
    resolution = input("Enter desired resolution (e.g., 720, 1080p, 4k, etc.): ").strip().lower()

    if resolution in resolution_map:
        myDict['format'] = f'bestvideo[height<={resolution_map[resolution]}]+bestaudio/best[height<={resolution_map[resolution]}]'
        print(f"Download quality set to: {resolution_map[resolution]}")
    else:
        print("Invalid resolution. Using default format: bestvideo+bestaudio")
    return myDict

def main():
    print("Welcome to MMX Multimedia Downloader v1.6!\n-----------------------------------------\nReport bugs, contribute and support the project at: https://github.com/shawafix/MMX-Multimedia-Downloader")

    download_options = {
        'format': 'bestvideo+bestaudio',
        'writesubtitles': False,
        'writeautomaticsub': FZZalse,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'srt',
        'writethumbnail': False,
        'outtmpl': '',
        'postprocessors': [],
        'ignoreerrors': True,
    }

    mode = input("Enter 1 for Advanced Download Options. Press ENTER to skip and proceed with Quick Download.\t")
    url = input("Enter Video or Playlist link: ")
    path = setPath()
    playlist_modifier = checkIfPlaylist(url)
    download_options['outtmpl'] = f"{path}{playlist_modifier}/%(title)s.%(ext)s"
    print(f"Output template: {download_options['outtmpl']}")

    checkIfAudio(download_options)
    if mode == '1':
        checkIfThumbnail(download_options)
        checkIfSubtitles(download_options)
        checkDownloadQuality(download_options)

    with yt_dlp.YoutubeDL(download_options) as ydl:
        try:
            ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            print(f"Skipping undownloadable video: {e}")

main()

