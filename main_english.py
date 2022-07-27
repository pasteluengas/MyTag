from itertools import tee
from tkinter import *
from tkinter import messagebox
import tkinter
from urllib.request import urlopen
from xml.etree.ElementTree import parse
import os.path as path
from mutagen.easyid3 import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TT2, TPE1, TRCK, TALB, USLT, error
import requests
import eyed3
from eyed3.id3.frames import ImageFrame
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os
import webbrowser


#Open Links Function
def callback(url):
    webbrowser.open_new(url)

#Tkinter app is created
app = tkinter.Tk()
app.geometry("460x500")
app.title("MyTag")
app.configure(bg='#FFFFFF')
app.resizable(0,0)

#here is saved the audio files from the selected folder
thefiles = []


MinOneFile = False

#Add text to console function
def create_label_console(w ,texts, color, size):
    count = len(app.winfo_children())
    label = tkinter.Label(w, text=f"-" + texts)
    label.configure(foreground=color, font = ("Terminal", size), bg="#000000")
    label.grid()

#Select Folder button function
def browse_button():
    global thefiles
    global filename
    
    #reestarts
    thefiles = []
    MinOneFile = False
    
    # The directory is saved in folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    content = os.listdir(filename)

    for fichero in content:
        if os.path.isfile(os.path.join(filename, fichero)):
            if fichero.endswith('.mp3') or fichero.endswith('.wav'):
                thefiles.append(fichero)
    print(thefiles)

#Download the album cover
def download_cover(url):
    f = open('cover.jpg','wb')
    print(url)
    response = requests.get(url)
    f.write(response.content)
    f.close()

#Search
def search():
    global MinOneFile
    songsWithoutFile = []
    album0 = searchAlbumEntry.get()
    artist0 = searchArtistEntry.get()

    #the spaces are replaced
    album1 = album0.replace(' ','%20')
    artist1 = artist0.replace(' ','%20')
    album1 = album1.replace('ü','%C3%BC')
    artist1 = artist1.replace('ü','%C3%BC')
    
    #the Last.Fm API is opened
    var_url = urlopen('http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=9431a6366225e88f9a1d9d0ce988e893&artist='+ artist1 +'&album='+ album1 +'&format=xml')
    xmldoc = parse(var_url)
    root = xmldoc.getroot()

    #Here MyTag gets the album, artist, and the album cover
    album = root[0][0].text
    artist = root[0][1].text
    imagelink = root[0][8].text

    #Console screen is created
    console = Toplevel()
    console.geometry("640x310")
    console.title(album + " - " + artist + " - Consola")
    console.configure(bg='#000000')
    
    #Image is downloaded
    download_cover(imagelink)

    #For each album's track
    for track in root.iter('track'):
        #Se obtiene el nombre del track
        nametrack = track.find('name').text
        #Se obtiene el numero de track
        numbertrack = track.get('rank')

        #For each audio file in folder
        for file in thefiles:
            songaaa = nametrack
            fileaaa = file.lower()
            songaaa = songaaa.lower()
            #songaaa is converted into an array that saves every word
            songaaa = songaaa.split(" ")
            nw = 0

            for w1 in songaaa: #for every word in songaaa
                w2 = w1.replace("'", "")
                w2 = w2.replace(",", "")
                print(w2)
                if w1 in fileaaa or w2 in fileaaa:
                    nw = nw + 1
                    if nw == len(songaaa): #Set the data
                        MinOneFile = True
                        tags = EasyID3(filename + "/" + file)
                        id3 = ID3(filename + "/" + file)
                        tags["title"] = nametrack
                        tags["artist"] = artist
                        tags["album"] = album
                        tags['tracknumber'] = numbertrack
                        tags.save()
                
                        #Se aplica el album cover
                        imagedata = open("cover.jpg", 'rb').read()
                        id3.add(APIC(3, 'image/jpeg', 3, 'Front cover', imagedata))
                        
                        #Se aplica el album cover
                        audiofile = eyed3.load(filename + "/" + file)
                        if (audiofile.tag == None):
                            audiofile.initTag()
                        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open('cover.jpg','rb').read(), 'image/jpeg')
                        audiofile.tag.save()

                        #It shows a text in screen when a song file is founded
                        create_label_console(console, "A file for " + nametrack + " was founded", "green", 10)
        
                else:
                    break

        

    print(str(folder_path))
    #If everything goes well
    if folder_path and MinOneFile:
        create_label_console(console, "The tags have been applied to the files we found", "green", 15)
    #If the folder don't have songs
    if not MinOneFile:
        create_label_console(console, "We didn't find any song", "red", 15)
        
    

            
            


folder_path = StringVar()                                                                                                         


#Here's the interface

chooseFolderlabel = Label(text="Select the folder where the audio files are located:")
chooseFolderlabel.grid(row= 0, column= 0, padx=10, pady=10)
chooseFolderlabel.config(fg = "#1556A4", bg = "#FFFFFF", font = ("Roboto Light", 15))


button2 = Button(text="Open Folder", command=browse_button)
button2.grid(row= 1, column= 0, padx=10, pady=10)
button2.config(bg = "#1556A4", relief=SUNKEN, bd=0, fg="#FFFFFF", width="11", height="1", font = ("Roboto Light", 10))
lbl1 = Label(master=app,textvariable=folder_path)
lbl1.grid(row= 2, column= 0, padx=10, pady=10)
lbl1.config(fg = "#1556A4", bg = "#FFFFFF", font = ("Roboto Light", 9))


AlbumNameLabel = tkinter.Label(app, text="Album's Name:")
AlbumNameLabel.grid(row= 3, column= 0, padx=10, pady=10)
AlbumNameLabel.config(fg = "#1556A4", bg = "#FFFFFF", font = ("Roboto Light", 15))

searchAlbumEntry = tkinter.Entry(app, width=50)
searchAlbumEntry.config(fg = "#000000", bg = "#FFFFFF", font = ("Roboto Light", 10))
searchAlbumEntry.grid(row= 4, column= 0, padx=10, pady=10)

ArtistNameLabel = tkinter.Label(app, text="Artist's Name:")
ArtistNameLabel.grid(row= 5, column= 0, padx=10, pady=10)
ArtistNameLabel.config(fg = "#1556A4", bg = "#FFFFFF", font = ("Roboto Light", 15))

searchArtistEntry = tkinter.Entry(app, width=50)
searchArtistEntry.grid(row= 6, column= 0, padx=10, pady=10)
searchArtistEntry.config(fg = "#000000", bg = "#FFFFFF", font = ("Roboto Light", 10))

searchButton = Button(app, text= "Set Data", command= search)
searchButton.grid(row= 7, column= 0, padx=10, pady=10)
searchButton.config(bg = "#1556A4", relief=SUNKEN, bd=0, fg="#FFFFFF", width="12", height="1", font = ("Roboto Light", 15))


link1 = Label(app, text="Report a bug", fg="#1556A4", bg="white", cursor="hand2")
link1.grid()
link1.bind("<Button-1>", lambda e: callback("https://pasteluengas.github.io/MyTag/index.html#Bug"))

Mark = Label(app, text='v1.0.0 | PasteLuengas')
Mark.grid(row=10, column=0, pady=50)
Mark.config(fg = "#000000", bg = "#FFFFFF")

#Comprobacion de Internet
try:
    request = requests.get("http://www.google.com", timeout=5)
except (requests.ConnectionError, requests.Timeout):
    messagebox.showinfo(message="It seems that you are not connected to the Internet, without it, this application will not work", title="Internet Error")


app.mainloop()
