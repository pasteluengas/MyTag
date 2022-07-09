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
from PIL import Image, ImageTk
import os

app = tkinter.Tk()
app.geometry("600x500")
app.title("MyTag")
app.configure(bg='#FFFFFF')
app.iconbitmap("C:\\Users\\Usuario\\ico\\icon.ico")

thefiles = []

def create_label_console(w ,texts, color, size):

    count = len(app.winfo_children())
    label = tkinter.Label(w, text=f"-" + texts)
    label.configure(foreground=color, font = ("Terminal", size), bg="#000000")
    label.grid()

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
    print(url)
    response = requests.get(url)
    f.write(response.content)
    f.close()

def search():
    songsWithoutFile = []
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

    console = Toplevel()
    console.geometry("640x310")
    console.title(album + " - " + artist + " - Consola")
    console.configure(bg='#000000')
    console.iconbitmap("C:\\Users\\Usuario\\ico\\icon.ico")
    
    

    #print(imagelink)
    #u = urlopen(imagelink)
    #raw_data= u.read()
    #u.close
    #photo= ImageTk.PhotoImage(data=raw_data)
    #label= tkinter.Label(console, image=photo)
    #label.image = photo
    #label.grid(row= 0, column= 0, padx=10, pady=10)
    

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

                create_label_console(console, "A file for  " + nametrack + " have been found", "green", 10)

            else:
                if nametrack in songsWithoutFile:
                    print("amogus")
                else:
                    songsWithoutFile.append(nametrack)
                    create_label_console(console, "No file found for " + nametrack, "red", 10)

    create_label_console(console, "The data has been applied to the files we found", "green", 15)

            
            


folder_path = StringVar()                                                                                                         

chooseFolderlabel = Label(text="Select the folder where the audio files are located:")
chooseFolderlabel.grid(row= 0, column= 0, padx=10, pady=10)
chooseFolderlabel.config(fg = "#1556A4", bg = "#FFFFFF", font = ("Roboto Light", 15))


button2 = Button(text="Open Folder", command=browse_button)
button2.grid(row= 1, column= 0, padx=10, pady=10)
button2.config(bg = "#1556A4", relief=SUNKEN, bd=0, fg="#FFFFFF", width="11", height="1", font = ("Roboto Light", 10))
lbl1 = Label(master=app,textvariable=folder_path)
lbl1.grid(row= 2, column= 0, padx=10, pady=10)
lbl1.config(fg = "#1556A4", bg = "#FFFFFF", font = ("Roboto Light", 9))


AlbumNameLabel = tkinter.Label(app, text="Album Name:")
AlbumNameLabel.grid(row= 3, column= 0, padx=10, pady=10)
AlbumNameLabel.config(fg = "#1556A4", bg = "#FFFFFF", font = ("Roboto Light", 15))

searchAlbumEntry = tkinter.Entry(app, width=50)
searchAlbumEntry.config(fg = "#000000", bg = "#FFFFFF", font = ("Roboto Light", 10))
searchAlbumEntry.grid(row= 4, column= 0, padx=10, pady=10)

ArtistNameLabel = tkinter.Label(app, text="Artist name:")
ArtistNameLabel.grid(row= 5, column= 0, padx=10, pady=10)
ArtistNameLabel.config(fg = "#1556A4", bg = "#FFFFFF", font = ("Roboto Light", 15))

searchArtistEntry = tkinter.Entry(app, width=50)
searchArtistEntry.grid(row= 6, column= 0, padx=10, pady=10)
searchArtistEntry.config(fg = "#000000", bg = "#FFFFFF", font = ("Roboto Light", 10))

searchButton = Button(app, text= "Set Data", command= search)
searchButton.grid(row= 7, column= 0, padx=10, pady=10)
searchButton.config(bg = "#1556A4", relief=SUNKEN, bd=0, fg="#FFFFFF", width="12", height="1", font = ("Roboto Light", 15))

Mark = Label(app, text='v0.5 Beta | PasteLuengas')
Mark.grid(row=12, column=0, pady=100)
Mark.config(fg = "#000000", bg = "#FFFFFF")

app.mainloop()