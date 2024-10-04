import yt_dlp
import yt_dlp.downloader
import termcolor
import tkinter as Tk
from tkinter import filedialog, messagebox
# & show available formats
def show_available_formats(url):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            print(f"{termcolor.colored("\n--------------Available formats (video + audio options):----------------- ",'light_green')}")
            for info in formats:
                format_id = info.get('format_id')    
                resolution = info.get('height', 'audio only')   
                ext = info.get('ext')  
                size = info.get('filesize_approx', 'unknow')
                print(f"{termcolor.colored("ID:",'light_green')} {termcolor.colored(f"{format_id}",'light_blue')} {termcolor.colored("Resolution:",'light_green')} {termcolor.colored(f"{resolution}",'light_blue')} {termcolor.colored("Extension:",'light_green')} {termcolor.colored(f"{ext}",'light_blue')} {termcolor.colored("Size:",'light_green')} {termcolor.colored(f"{size}",'light_blue')}")
            return formats     
    except Exception as e:
        print(f"{termcolor.colored(f"Error in fetch formats: {e}",'red')}")
        return []
# & END available formats
# ~ downloading video or audio and specified format
def Download_video(url, options):
    
    try:
        ydl_opts = {
            'outtmpl': f"{options['output_path']}/%(title)s.%(ext)s",
            'format': f"{options['format']}",
            'postprocessors': options.get('postprocessors', []),
            'merge_output_format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
           print(f"{termcolor.colored(f"Downloading video from: {url}","light_yellow")}")
           ydl.download([url])
           print(f"{termcolor.colored("Download completed !","green")}")
           
    except Exception as e:
        print(f"error happen : {termcolor.colored(f"{e}",'red')}")

 # ? download playlist videos and audio anly
def download_playlist_videos(url, options):
    # Create a list of video indices to download
    video_indices = range(options['playliststart'], options['playlistend'] + 1)

    # Create a comma-separated string of the indices to pass to yt-dlp
    playlist_items = ",".join(map(str, video_indices))

    ydl_opts = {
        'outtmpl': f"{options['output_path']}/%(playlist_index)s - %(title)s.%(ext)s",
        'format': f"{options['format']}",
        'noplaylist': False,  # Set to False to allow playlist download
        'playlist_items': playlist_items,  # Specify the exact videos to download by index
        'postprocessors': options.get('postprocessors', []),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(termcolor.colored(f"\nDownloading playlist from video {options['playliststart']} to {options['playlistend']}...", 'light_yellow'))
            ydl.download([url])  # Download the videos specified in playlist_items
            print(termcolor.colored("Download completed!", "green"))
    except Exception as e:
        print(f"{termcolor.colored(f'Error: {e}', 'red')}")


# ? download_options
def download_options(url):
    
    print(f"{termcolor.colored("--------------------Choose your download options:----------------------","light_blue")}")
    # download options
    print(termcolor.colored("1-Video best quality(Video + audio)",'light_magenta'))
    print(termcolor.colored("2-download by Format ID(you decide by entre : ID_video+ID_audio)",'light_magenta'))
    print(termcolor.colored("3-Audio(MP3)(Best quality)",'light_magenta'))
    print(termcolor.colored("4-Download playlist video with specific range",'light_magenta'))
    print(termcolor.colored("5-Download playlist audio with specific range",'light_magenta'))
    
    print(f"{termcolor.colored("----------------------------------------------------------------------","light_blue")}")
    choice = input(f"{termcolor.colored("Entre choice(1 or 2 or 3 or 4 or 5): ",'light_yellow')}").strip()
    if str(choice) == '1':
          format = 'bestvideo+bestaudio/best[height<=1080]'
          postprocessors = []
          output_path = input(f"{termcolor.colored("Enter the output directory (leave blank for current directory or '.'): ",'light_yellow')}").strip()
          return {
        'format': format,
        'postprocessors': postprocessors,
        'output_path': output_path,
        }
    elif str(choice) == '2':
        # ! show formats
        print(f"{termcolor.colored("--------------------Available formats (video + audio options):--------------------", 'light_blue')}")
        show_available_formats(url)
        format_id = input(termcolor.colored("Enter the format ID you want to download(for dowload video format id must be e.g: 223+555): ", 'light_yellow')).strip()
        format = f'{str(format_id)}'
        postprocessors = []
        output_path = input(f"{termcolor.colored("Enter the output directory (leave blank for current directory or '.'): ",'light_yellow')}").strip()
        return {
        'format': format,
        'postprocessors': postprocessors,
        'output_path': output_path,
    }
    elif str(choice) == '3':
          format = 'bestaudio/best'
          postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
          }]
          output_path = input(f"{termcolor.colored("Enter the output directory (leave blank for current directory or '.'): ",'light_yellow')}").strip()
          return {
            'format': format,
            'postprocessors': postprocessors,
            'output_path': output_path,
          }
    elif str(choice) == '4':
       playlist_start = input(termcolor.colored("Enter the starting video number (leave blank for start): ", 'light_yellow')).strip() or '1'
       playlist_end = input(termcolor.colored("Enter the ending video number (leave blank for the end): ", 'light_yellow')).strip() or None
       resolution = input(termcolor.colored("Enter resolution (144,240,360,480,720,1080) without 'p': ", 'light_yellow')).strip()

       # Validate resolution input
       valid_resolutions = ['144','240','360', '480', '720', '1080']
       if resolution not in valid_resolutions:
            print(termcolor.colored(f" Invalid resolution '{resolution}'.", 'red'),termcolor.colored("defaulting to 1080p.......",'light_cyan'))
            resolution = '1080' # ~ make resolution default on 1080p

       # Exclude format_id=251 for audio
       format_id = f'bestvideo[height<={resolution}]+bestaudio[format_id!=251]/best[height<={resolution}][format_id!=251]'
       postprocessors = []
       output_path = input(f"{termcolor.colored("Enter the output directory (leave blank for current directory or '.'): ",'light_yellow')}").strip()
       return {
                'format': format_id,
                'postprocessors': postprocessors,
                'output_path': output_path,
                'noplaylist': False,
                'playliststart': int(playlist_start),
                'playlistend': int(playlist_end) if playlist_end else None
        }
    elif str(choice) == '5':
       playlist_start = input(termcolor.colored("Enter the starting Audio number (leave blank for start): ", 'light_yellow')).strip() or '1'
       playlist_end = input(termcolor.colored("Enter the ending Audio number (leave blank for the end): ", 'light_yellow')).strip() or None
       format_id = 'bestaudio/best'
       postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }] 
       output_path = input(f"{termcolor.colored("Enter the output directory (leave blank for current directory or '.'): ",'light_yellow')}").strip()
       return {
            'format': format_id,
            'postprocessors': postprocessors,
            'output_path': output_path,
            'noplaylist': False,
            'playliststart': int(playlist_start),
            'playlistend': int(playlist_end) if playlist_end else None
        }
    else:
        print(f"{termcolor.colored("invalid option,Defaulting to choice 1.",'red')}")
        format = 'bestvideo+bestaudio/best[height<=1080]'
        postprocessors = []
        return {
        'format': format,
        'postprocessors': postprocessors,
        'output_path': output_path,
        }
    

# ? -----------END download_options-----------
# ~ run main file
if __name__ == "__main__":
    while True:
        video_url = input(termcolor.colored("Enter video or playlist URL(for exit write: exit): ", 'light_blue')).strip()
        if video_url.lower() == 'exit':
            print(termcolor.colored('Thanks for use aratube downloader script ','green'))
            break
        options = download_options(video_url)

        if options:
            # If the user has chosen to download a playlist
            if 'playliststart' in options and 'playlistend' in options and 'noplaylist' in options:
                download_playlist_videos(video_url, options)
            else:
                Download_video(video_url, options)

