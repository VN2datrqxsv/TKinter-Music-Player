#!/usr/bin/python3
"""
Using the tkinter and pygame modules to create GUI based music player. It includes
audio controls powered by the pygame.mixer, dynamic playlist search and management
using a listbox, that also remain unchanged after closing the program. Uses system
operations to load audio files from local directory.
"""

from tkinter import *
from tkinter.ttk import *
import pygame
import os

DEBUG = True


class MusicPlayer:
    """One object of this class represents a tkinter GUI application that plays
    audio files and can write and read a .m3u playlist."""

    def __init__(self, root):
        """Creates a tkinter GUI application that plays audio files and
        can write and read a .m3u playlist."""
        self.playlistfilename = 'playlist.m3u'
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("1000x200+200+200")
        pygame.init()
        pygame.mixer.init()
        self.track = StringVar()
        self.status = StringVar()
        self.exception = StringVar()

        # Creating trackframe for songtrack label & trackstatus label
        trackframe = LabelFrame(self.root, text="Song Track", relief=GROOVE)
        trackframe.place(x=0, y=0, width=600, height=100)
        # Making the self.track the textvariable for songtrack and
        # the self.status the textvariable for trackstatus frames.
        self.songtrack = Label(trackframe, textvariable=self.track).grid(
            row=0, column=0, padx=10, pady=5)
        self.trackstatus = Label(trackframe, textvariable=self.status).grid(
            row=0, column=1, padx=10, pady=5)
        self.trackexception = Label(trackframe, textvariable=self.exception).grid(
            row=0, column=2, padx=10, pady=5)

        # Creating buttonframe
        buttonframe = LabelFrame(
            self.root, text="Control Panel", relief=GROOVE)
        # Inserting song control Buttons
        buttonframe.place(x=0, y=100, width=600, height=100)
        Button(buttonframe, text="Play", command=self.playsong).grid(
            row=0, column=0, padx=10, pady=5)
        Button(buttonframe, text="Pause", command=self.pausesong
               ).grid(row=0, column=1, padx=10, pady=5)
        Button(buttonframe, text="Unpause", command=self.unpausesong
               ).grid(row=0, column=2, padx=10, pady=5)
        Button(buttonframe, text="Stop", command=self.stopsong).grid(
            row=0, column=3, padx=10, pady=5)
        # Inserting playlist control Buttons
        Button(buttonframe, text="Load Playlist",
               command=self.loadplaylist).grid(row=1, column=0, padx=10, pady=5)
        Button(buttonframe, text="Save Playlist",
               command=self.saveplaylist).grid(row=1, column=1, padx=10, pady=5)
        Button(buttonframe, text="Remove Song",
               command=self.removesong).grid(row=1, column=2, padx=10, pady=5)
        Button(buttonframe, text="Refresh From Folder",
               command=self.refresh).grid(row=1, column=3, padx=10, pady=5)

        # Creating songs' frame
        songsframe = LabelFrame(self.root, text="Song Playlist", relief=GROOVE)
        songsframe.place(x=600, y=0, width=400, height=150)
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set,
                                selectbackground="gold",
                                selectmode=SINGLE, relief=GROOVE)
        # Applying Scrollbar to playlist Listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)

        # Adding playlist search controls
        searchframe = LabelFrame(self.root, relief=GROOVE)
        searchframe.place(x=600, y=145, width=400, height=50)
        search_input = Entry(searchframe, width=30)
        self.inputVar = StringVar()
        #Below makes the self.inputVar the textvariable for search_input
        search_input.config(textvariable=self.inputVar)

        search_input.grid(row=1, column=1, padx=1, pady=1)
        #binds Return key to call self.search
        Button(searchframe, text="Search",
               command=self.search).grid(row=1, column=2, padx=1, pady=1)
        search_input.bind('<Return>', self.search)

        # Changing directory for fetching songs using absolute path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        music_dir = os.path.join(script_dir, "music")
        os.chdir(music_dir)
        # Inserting songs into playlist
        self.refresh()

    def search(self, *args):
        """
        Removes from the self.playlist ListBox any filename that does not
        partially match the characters from the self.inputVar of the
        search_input Entry widget.
        """
        try:
            items = self.playlist.get(0, END)
            found_items = [
                item for item in items if self.inputVar.get().strip().casefold()
                in item.casefold()]
        except:
            self.status.set("File Not Found")
            return
        else:
            self.playlist.delete(0, END)
            for index, item in enumerate(found_items):
                self.playlist.insert(index, item)

    def playsong(self):
        """Displays selected song and its playing status and plays the song."""
        self.track.set(self.playlist.get(ACTIVE))
        self.status.set("-Playing")
        self.exception.set("")
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        pygame.mixer.music.play()

    def stopsong(self):
        """Displays stopped status and stops the song."""
        self.status.set("-Stopped")
        self.exception.set("")
        pygame.mixer.music.stop()

    def pausesong(self):
        """Displays the paused status and pauses the song."""
        self.status.set("-Paused")
        self.exception.set("")
        pygame.mixer.music.pause()

    def unpausesong(self):
        """Displays the playing status and unpauses the song."""
        self.status.set("-Playing")
        self.exception.set("")
        pygame.mixer.music.unpause()

    def removesong(self):
        """Deletes the active song from the playlist."""
        self.playlist.delete(ACTIVE)

    def loadplaylist(self):
        """
        Clears the current playlist and loads a previously saved playlist
        from the music folder. A user friendly message is appended to the status
        if a FileNotFoundError is caught.
        All other exception messages are
        appended to the status in their default string form.
        Ignore the lines that start with #.
        """
        # Clearing the search_input Entry widget via self.inputVar
        try:
            self.inputVar.set("")
            self.playlist.delete(0, END)
            with open(self.playlistfilename, "r+") as f:
                tmp = f.read()
            temp = "\n".join(tmp.splitlines()[1:])
            temp = temp.splitlines()
            for file in temp:
                self.playlist.insert("end", file)
            del tmp
            del temp
        except:
            self.exception.set(f"file {self.playlistfilename} not found")
            return

    def saveplaylist(self):
        """
        Saves the current playlist to the playlist file in the music
        folder. All exception messages are appended to the status in their
        default string form.
        Making sure the first line of the file is only:
        #EXTM3U
        """
        tmp = self.playlist.get(0, END)
        temp = "\n".join(str(x) for x in tmp)
        with open(f"{self.playlistfilename}", "w") as f:
            f.write("#EXTM3U\n")
            f.write(f"{temp}")
        del tmp
        del temp

    def refresh(self):
        """
        Clears the current playlist and fills it with all valid sound files
        from the music folder. All exception messages are appended to the status
        in their default string form.
        """
        self.inputVar.set("") # Clearing the search_input Entry widget via self.inputVar
        self.playlist.delete(0, END)
        templist = os.listdir()
        templist = [x for x in templist if not x.startswith('.')]
        templist = [x for x in templist if x.endswith(
            (".mp3", ".ogg", ".wav"))]
        for index, file in enumerate(templist):
            self.playlist.insert(index, file)


def main():
    """Create main window and start a MusicPlayer application on it."""
    # Creating TK root window
    root = Tk()
    # Passing root to the MusicPlayer constructor
    app = MusicPlayer(root)
    # Start the main GUI loop
    root.mainloop()


if __name__ == "__main__":
    main()
