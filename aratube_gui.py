import yt_dlp
import tkinter as Tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for both dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

image_path = resource_path("images/arata.jpg")

# * ---- START CODING PART OF GUI --------------
# GUI Functions
def show_available_formats_gui(url):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            format_list = []

            for info in formats:
                format_id = info.get('format_id')
                resolution = info.get('height', 'audio only')
                ext = info.get('ext')
                size = info.get('filesize_approx', 'unknown')
                format_list.append(f"ID: {format_id} | Resolution: {resolution} | Extension: {ext} | Size: {size}")
            
            return format_list
    except Exception as e:
        messagebox.showerror("Error", f"Error in fetching formats: {e}")
        return []

def download_video_gui(url, options):
    try:
        ydl_opts = {
            'outtmpl': f"{options['output_path']}/%(title)s.%(ext)s",
            'format': f"{options['format']}",
            'postprocessors': options.get('postprocessors', []),
            'merge_output_format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            messagebox.showinfo("Success", "Download completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {e}")
        
def download_playlist_videos_gui(url, options):
    video_indices = range(options['playliststart'], options['playlistend'] + 1)
    playlist_items = ",".join(map(str, video_indices))

    ydl_opts = {
        'outtmpl': f"{options['output_path']}/%(playlist_index)s - %(title)s.%(ext)s",
        'format': f"{options['format']}",
        'noplaylist': False,
        'playlist_items': playlist_items,
        'postprocessors': options.get('postprocessors', []),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {e}")

# GUI Interface
def ara_tube_gui():
    def download_button_click():
        url = url_entry.get()
        output_path = output_dir.get()

        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        if download_type.get() == "1-Video best quality":
            options = {
                'format': 'bestvideo+bestaudio/best[height<=1080]',
                'postprocessors': [],
                'output_path': output_path
            }
            download_video_gui(url, options)

        elif download_type.get() == "2-Download by Format ID":
            format_id = format_entry.get()
            if not format_id:
                messagebox.showerror("Error", "Please enter a format ID.")
                return
            options = {
                'format': format_id,
                'postprocessors': [],
                'output_path': output_path
            }
            download_video_gui(url, options)

        elif download_type.get() == "3-Audio only":
            options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }],
                'output_path': output_path
            }
            download_video_gui(url, options)

        elif download_type.get() == "4-Download playlist (specific range, video)":
            playlist_start = int(playlist_start_entry.get() or '1')
            playlist_end = int(playlist_end_entry.get() or '1')
            resolution = resolution_entry.get() or '1080'
            options = {
                'format': f'bestvideo[height<={resolution}]+bestaudio',
                'postprocessors': [],
                'output_path': output_path,
                'noplaylist': False,
                'playliststart': playlist_start,
                'playlistend': playlist_end
            }
            download_playlist_videos_gui(url, options)

        elif download_type.get() == "5-Download playlist (specific range, audio)":
            playlist_start = int(playlist_start_entry.get() or '1')
            playlist_end = int(playlist_end_entry.get() or '1')
            options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }],
                'output_path': output_path,
                'noplaylist': False,
                'playliststart': playlist_start,
                'playlistend': playlist_end
            }
            download_playlist_videos_gui(url, options)

    def browse_output_dir():
        directory = filedialog.askdirectory()
        if directory:
            output_dir.set(directory)

    def on_download_type_change(*args):
        choice = download_type.get()

        # Hide all frames initially
        format_frame.grid_forget()
        resolution_frame.grid_forget()
        playlist_options_frame.grid_forget()

        if choice == "2-Download by Format ID":
            format_frame.grid(row=5, column=1, padx=5, pady=5)
            show_formats_button.grid(row=6, column=1, padx=5, pady=5)
            formats_text.grid(row=7, column=1, padx=5, pady=5)
        else:
            show_formats_button.grid_forget()
            formats_text.grid_forget()

        if choice == "4-Download playlist (specific range, video)" or choice == "5-Download playlist (specific range, audio)":
            playlist_options_frame.grid(row=8, column=1, columnspan=2)
            if choice == "4-Download playlist (specific range, video)":
                resolution_frame.grid(row=4, column=1, padx=5, pady=5)
                # Move the playlist start and end entries below the resolution choice
                playlist_start_label.grid(row=9, column=1, padx=5, pady=5)
                playlist_start_entry.grid(row=9, column=2, padx=5, pady=5)
                playlist_end_label.grid(row=10, column=1, padx=5, pady=5)
                playlist_end_entry.grid(row=10, column=2, padx=5, pady=5)


    def show_formats():
        url = url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        formats = show_available_formats_gui(url)
        formats_text.delete(1.0, Tk.END)
        if formats:
            formats_text.insert(Tk.END, "\n".join(formats))

    # Create the main window
    root = Tk.Tk()
    root.title("~Ara Tube Downloader")
    root.geometry("800x600")
    # Set background image
    background_image = ImageTk.PhotoImage(Image.open("images/arata.jpg"))
    background_label = Tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)
    # Disable window resizing
    root.resizable(False, False)



    # URL Input
    Tk.Label(root, text="Video/Playlist URL:",bg='black', fg='white').grid(row=0, column=0, sticky=Tk.W)
    url_entry = Tk.Entry(root, width=50,bg='black', fg='white')
    url_entry.grid(row=0, column=1, padx=5, pady=5)

    # Output Directory
    Tk.Label(root, text="Output Directory:", bg='black', fg='white').grid(row=1, column=0, sticky=Tk.W)
    output_dir = Tk.StringVar()
    Tk.Entry(root, textvariable=output_dir, bg='black', fg='white', width=50).grid(row=1, column=1, padx=5, pady=5)
    Tk.Button(root, text="Browse",bg='black', fg='white', command=browse_output_dir).grid(row=1, column=2, padx=5, pady=5)

    # Download Type
    Tk.Label(root, text="Download Type:",bg='black',fg='white').grid(row=2, column=0, sticky=Tk.W)
    download_type = Tk.StringVar(value="1-Video best quality")
    download_type.trace("w", on_download_type_change)
    # Create the OptionMenu and store it in a variable to modify its properties
    download_type_menu = Tk.OptionMenu(root, download_type, 
                                   "1-Video best quality", 
                                   "2-Download by Format ID", 
                                   "3-Audio only", 
                                   "4-Download playlist (specific range, video)", 
                                   "5-Download playlist (specific range, audio)")

    # Configure the OptionMenu background and foreground colors
    download_type_menu.config(bg='black', fg='white', activebackground='black', activeforeground='white')

    # Place the OptionMenu using grid
    download_type_menu.grid(row=2, column=1, padx=5, pady=5)
    # Format Input (only for Download by Format ID)
    format_frame = Tk.Frame(root)
    Tk.Label(format_frame, text="Format ID:",bg='black',fg='white').grid(row=0, column=0)
    format_entry = Tk.Entry(format_frame, width=30, bg='black', fg='white')
    format_entry.grid(row=0, column=1)

    # Show Formats Button (only for Download by Format ID)
    show_formats_button = Tk.Button(root, text="Show Available Formats",bg='black',fg='white', command=show_formats)

    # Text widget to display available formats
    formats_text = scrolledtext.ScrolledText(root, height=10, width=60)
    formats_text.config(bg='black', fg='white')

    # Resolution Input (only for playlist video range)
    resolution_frame = Tk.Frame(root,bg='black')
    Tk.Label(resolution_frame, text="Resolution (144, 240, 360, 480, 720, 1080):",bg='black',fg='white').grid(row=0, column=0)
    resolution_entry = Tk.Entry(resolution_frame,bg='black',fg='white', width=10)
    resolution_entry.grid(row=0, column=1)

    # Playlist Start/End Frame
    playlist_options_frame = Tk.Frame(root, bg='black')
    playlist_start_label = Tk.Label(playlist_options_frame, text="Start at video:", bg='black', fg='white')
    playlist_start_label.grid(row=0, column=0, padx=5, pady=5)
    playlist_start_entry = Tk.Entry(playlist_options_frame, width=5, bg='black', fg='white')
    playlist_start_entry.grid(row=0, column=1, padx=5, pady=5)
    playlist_end_label = Tk.Label(playlist_options_frame, text="End at video:", bg='black', fg='white')
    playlist_end_label.grid(row=1, column=0, padx=5, pady=5)
    playlist_end_entry = Tk.Entry(playlist_options_frame, width=5, bg='black', fg='white')
    playlist_end_entry.grid(row=1, column=1, padx=5, pady=5)

    # Download Button
    Tk.Button(root, text="Download",bg='black',fg='white', command=download_button_click).grid(row=10, column=1, padx=5, pady=5)
    # Start GUI loop
    root.mainloop()

# Main Program Execution
if __name__ == "__main__":
    
    ara_tube_gui()
