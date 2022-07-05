from itertools import tee
from tkinter import *
import tkinter
from urllib.request import urlopen
from xml.etree.ElementTree import parse
import os.path as path
from mutagen.easyid3 import EasyID3
import requests
import eyed3
from eyed3.id3.frames import ImageFrame
from tkinter import filedialog
from tkinter import ttk
import os

thefiles = []

def browse_button():
    global thefiles
    global filename
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    #print(filename)
    content = os.listdir(filename)
    #print(content)

    for fichero in content:
        if os.path.isfile(os.path.join(filename, fichero)):
            if fichero.endswith('.mp3') or fichero.endswith('.wav'):
                thefiles.append(fichero)
    print(thefiles)


def download_cover(url):
    f = open('cover.jpg','wb')
    response = requests.get(url)
    f.write(response.content)
    f.close()

def search():
    album0 = searchAlbumEntry.get()
    artist0 = searchArtistEntry.get()
    album1 = album0.replace(' ','%20')
    artist1 = artist0.replace(' ','%20')
    var_url = urlopen('http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=9431a6366225e88f9a1d9d0ce988e893&artist='+ artist1 +'&album='+ album1 +'&format=xml')
    xmldoc = parse(var_url)
    root = xmldoc.getroot()
    album = root[0][0].text
    artist = root[0][1].text
    imagelink = root[0][8].text
    print(imagelink)
    download_cover(imagelink)
    for track in root.iter('track'):
        nametrack = track.find('name').text
        numbertrack = track.get('rank')
        #print(numbertrack + ". " + nametrack)
        #print(track.tag, track.attrib)
        #print(nametrack)

        for file in thefiles:
            print(filename)
            #print("if " + nametrack.lower() + " in " + file.lower())
            if nametrack.lower() in file.lower():
                #print("aaa")
                print("tags = EasyID3(" + filename + "/" + file + ".mp3)")
                tags = EasyID3(filename + "/" + file)
                tags["title"] = nametrack
                tags["artist"] = artist
                tags["album"] = album
                tags['tracknumber'] = numbertrack
                tags.save()
                #A partir de aqui me quiero morir
                audiofile = eyed3.load(filename + "/" + file)
                print(file + "hola")
                if (audiofile.tag == None):
                    audiofile.initTag()
                audiofile.tag.images.set(ImageFrame.FRONT_COVER, open('cover.jpg','rb').read(), 'image/jpeg')
                audiofile.tag.save()
            else:
                hola = "hola"
                #print("No se enontró archivo MP3 para " + nametrack)
    #print(album + ", " + artist)

app = tkinter.Tk()
app.geometry("1000x500")

app.configure(bg='#1C003F')

folder_path = StringVar()                                                                                                         

chooseFolderlabel = Label(text="Seleccione la carpeta donde se encuentran los archivos de audio:")
chooseFolderlabel.grid(row= 0, column= 0, padx=10, pady=10)
chooseFolderlabel.config(fg = "White", bg = "#1C003F", font = ("Microsoft JhengHei Light", 15))

button2 = Button(text="Browse", command=browse_button)
button2.grid(row= 1, column= 0, padx=10, pady=10)
button2.config(bg = "#4800A4", relief=SUNKEN, bd=0, fg="white", width="7", height="1", font = ("Microsoft JhengHei Light", 10))
lbl1 = Label(master=app,textvariable=folder_path)
lbl1.grid(row= 2, column= 0, padx=10, pady=10)
lbl1.config(fg = "White", bg = "#1C003F", font = ("Microsoft JhengHei Light", 9))


AlbumNameLabel = tkinter.Label(app, text="Nombre del album:")
AlbumNameLabel.grid(row= 3, column= 0, padx=10, pady=10)
AlbumNameLabel.config(fg = "White", bg = "#1C003F", font = ("Microsoft JhengHei Light", 15))

searchAlbumEntry = tkinter.Entry(app, width=50)
searchAlbumEntry.grid(row= 4, column= 0, padx=10, pady=10)

ArtistNameLabel = tkinter.Label(app, text="Nombre del artista:")
ArtistNameLabel.grid(row= 5, column= 0, padx=10, pady=10)
ArtistNameLabel.config(fg = "White", bg = "#1C003F", font = ("Microsoft JhengHei Light", 15))

searchArtistEntry = tkinter.Entry(app, width=50)
searchArtistEntry.grid(row= 6, column= 0, padx=10, pady=10)

searchButton = Button(app, text= "Get Data", command= search)
searchButton.grid(row= 7, column= 0, padx=10, pady=10)
searchButton.config(bg = "#4800A4", relief=SUNKEN, bd=0, fg="white", width="12", height="1", font = ("Microsoft JhengHei Light", 15))

app.mainloop()