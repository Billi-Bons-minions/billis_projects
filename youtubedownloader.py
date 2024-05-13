from pytube import YouTube
import tkinter as tk
from tkinter.ttk import *
from moviepy.editor import *
import os
nurTon = 0
nurton = 0
def nursounddownload():
    yt = YouTube(textbox.get())
    textbox.delete(0, "end")
    video = yt.streams.get_highest_resolution()
    out_file = video.download()
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    videoclip = VideoFileClip(out_file)
    audioclip = videoclip.audio
    audioclip.write_audiofile(new_file)
    videoclip.close()
    audioclip.close()
    os.remove(out_file)
def videodownload():
    yt = YouTube(textbox.get())
    video = yt.streams.get_highest_resolution()
    video.download()
def nur_sound():
    global nurTon, nurton
    if nurTon.get() == 1:
        nurton = True
    elif nurTon.get() == 0:
        nurton = False

def download():
    global nurton
    if nurton == True:
        nursounddownload()
    elif nurton == False:
        videodownload()

main = tk.Tk()
main.geometry("250x117")
main.resizable(False,False)
main.title("YT-Downloader")
text = tk.Label(main, text="Enter your url")
text.pack()
textbox = tk.Entry(main)
textbox.pack()
nurTon = tk.IntVar()
nursound = tk.Checkbutton(main, text="Nur Ton", onvalue=1, offvalue=0,variable=nurTon,command=nur_sound)
nursound.pack()
button = tk.Button(main, text="Download", command=download)
button.pack()
bar = Progressbar(main, orient="horizontal", length=225)
bar.pack()
main.mainloop()