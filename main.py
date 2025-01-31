import yt_dlp
from tkinter import filedialog

mmx_metadata = {  # local specifics
    'download_path': '',
    'playlist_path_modifier': '',  # will change to %(playlist_title)s if the link was found to be a playlist
}

download_options = {  # yt-dlp specifics
    'format': 'bestvideo+bestaudio',
    'writesubtitles': False,
    'writeautomaticsub': False,
    'subtitleslangs': ['en'],
    'subtitlesformat': 'srt',
    'writethumbnail': False,
    'outtmpl': '',  # this will be set dynamically
    'postprocessors': [],
    'ignoreerrors': True,
}

def setPath():
    path = filedialog.askdirectory()
    print(f"Download path set to: {path}")  # Debugging print
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
        isThumb = int(input("Enter 1 for thumbnail download, press ENTER button to skip:\t"))
        if isThumb == 2:
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

def main(ydl_dict):
    print("Welcome to MMX Multimedia Downloader v1.5.1!\n-----------------------------------------\nReport bugs, contribute and support the project at: <will add link when set up>")
    mode = input("Enter 1 for Advanced Download Options. Press ENTER to skip and proceed with Quick Download.\t")
    url = input("Enter Video or Playlist link:")
    path = setPath()
    playlist_modifier = checkIfPlaylist(url)
    ydl_dict['outtmpl'] = f"{path}{playlist_modifier}/%(title)s.%(ext)s"
    print(f"Output template: {ydl_dict['outtmpl']}")  # Debugging print

    checkIfAudio(ydl_dict)
    if mode == '1':
        checkIfThumbnail(ydl_dict)
        checkIfSubtitles(ydl_dict)

    with yt_dlp.YoutubeDL(ydl_dict) as ydl:
        try:
            ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            print(f"Skipping undownloadable video: {e}")

    return ydl_dict

try:
    main(download_options)
except Exception as e:
    print(f"An error occurred during the download process: {e}")

