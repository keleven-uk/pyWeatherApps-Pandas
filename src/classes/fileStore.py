###############################################################################################################
#    fileStore.py   Copyright (C) <2025>  <Kevin Scott>                                                       #
#                                                                                                             #
#    A class that acts has a wrapper around a dictionary access.                                              #
#    The items to store are song files,                                                                       #
#      The key is either made up of {song.artist}:{tag.title}                                                 #
#        or soundex({song.artist}:{tag.title})                                                                #
#        or any unique token generated from the song.                                                         #
#      The data is a list [songFile, songDuration, ignore flag]                                               #
#                                                                                                             #
#    Uses pickle or json to load and save the library.                                                        #
#    The format is specified when the library is created.                                                     #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2020-2022>  <Kevin Scott>                                                                 #
#                                                                                                             #
#    This program is free software: you can redistribute it and/or modify it under the terms of the           #
#    GNU General Public License as published by the Free Software Foundation, either Version 3 of the         #
#    License, or (at your option) any later Version.                                                          #
#                                                                                                             #
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without        #
#    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#    GNU General Public License for more details.                                                             #
#                                                                                                             #
#    You should have received a copy of the GNU General Public License along with this program.               #
#    If not, see <http://www.gnu.org/licenses/>.                                                              #
#                                                                                                             #
###############################################################################################################

import os
import pickle

import src.timer as timer
import src.Exceptions as myExceptions


class FileStore():
    """  A simple class that wraps the library dictionary.

         usage:
         songLibrary = myLibrary.Library(name, format)
            name = name of datebase
            format = format used to save database = either pickle or json.

         to add an item              - songLibrary.addItem(key, musicFile, musicDuration) - Data specific.
         to retrieve an item         - songFile, songDuration, songDuplicate = songLibrary.getItem(key) - Data specific.
         to test for key             - if songLibrary.hasKey(key):
         to return number of items   - l = songLibrary.noOfItems()
         to test database integrity  - songLibrary.check("test") - Data specific.
         to prune database           - songLibrary.check("delete")
         to load items               - songLibrary.load()
         to save items               - songLibrary.save()

         TODO - possibly needs error checking [some done, some to go].
    """

    #__slots__ = ["library", "timer", "filename", "format", "__overWrite"]

    def __init__(self, dataPath):
        self.dataPath    = dataPath
        self.fileName    = dataPath / "fileStore.pickle"
        self.timer       = timer.Timer()                #  A timer class.

        self.__load()

    #---------------------------------------------------------------------------------------------- __listFiles() -----------------------
    def checkNewFiles(self):
        """  Produce a list of weather data files in the data directory.
             Returns the number of the new files and a list of their file paths.
        """
        dataFiles = self.dataPath.rglob("*.xlsx")
        newFiles  = 0
        filePaths = []

        for file in dataFiles:
            if not self.hasKey(file):
                self.addItem(file, False)
                newFiles += 1
                filePaths.append(file)

        return (newFiles, filePaths)
    #---------------------------------------------------------------------------------------------- hasKey(self, key) -----------------------
    def hasKey(self, key):
        """  Returns true if the key exist in the fileStore.
        """
        return key in self.fileStore
    #---------------------------------------------------------------------------------------------- addItem(self, key, item1 -----------------
    def addItem(self, key, item1):
        """  Adds to the fileStore, the key is a path.
             item1 is set to False, this indicates is has been added but not processed.
        """
        self.fileStore[key] = [item1]

    def getItem(self, key):
        """  Returns items at position key from the library.
        """
        if self.hasKey(key):
            return self.library[key]
        else:
            raise myExceptions.LibraryError

    def delItem(self, key):
        """  Deletes item at position key from the library.
        """
        try:
            del self.library[key]
        except (KeyError):
            raise myExceptions.LibraryError from None

    @property
    def noOfItems(self):
        """  Return the number of entries in the fileStore
        """
        if not self.fileStore:
            self.load()
        return len(self.fileStore)

    #---------------------------------------------------------------------------------------------- save(self) -----------------------
    def save(self):
        """  Save the fileStore in pickle format.
        """
        with open(self.fileName, "wb") as pickle_file:
            pickle.dump(self.fileStore, pickle_file)
    #---------------------------------------------------------------------------------------------- __load(self) -----------------------
    def __load(self):
        """  Loads the fileStore from disc.
        """
        try:
            with open(self.fileName, "rb") as pickle_file:
                self.fileStore = pickle.load(pickle_file)
        except FileNotFoundError:
            print(f"ERROR :: Cannot find library file. {self.fileName}.  Will use an empty library")
            self.fileStore = {}



    def clear(self):
        """  Clears the library.
        """
        self.library.clear()

    def check(self, mode, logger=None):
        """  Runs a database data integrity check.

             If a logger is passed in, then use it - else ignore.
        """
        self.timer.Start()        #  Start timer.
        missing   = 0
        removed   = 0

        if logger:
            logger.info("-" * 100)

        self.displayMessage(f"Running database integrity check on {self.filename} in {mode} mode", logger)
        self.displayMessage(f"Loading {self.filename}", logger)

        if not self.library:
            try:
                self.load()
            except FileNotFoundError:
                raise myExceptions.LibraryError from None

        no_songs = self.noOfItems
        self.displayMessage(f"Song Library has {no_songs} songs", logger)

        for song in self.library.copy():  # iterate over a copy, gets around the error dictionary changed size during iteration
            path, duration, ignore = self.getItem(song)
            if not os.path.isfile(path):
                if mode == "delete":
                    self.delItem(song)
                    print(f"Deleting {path}")
                    removed += 1
                else:
                    missing += 1
                    print(f"Song does not exist {path}")

        timeStop = self.timer.Stop      #  Stop timer.

        if removed:
            self.displayMessage(f"Saving {self.filename}", logger)
            self.save()
            self.displayMessage(f"Completed  :: {timeStop} and removed {removed} entries from database.", logger)
            no_songs = self.noOfItems
            self.displayMessage(f"Song Library has now {no_songs} songs", logger)
        else:
            if missing:
                self.displayMessage(f"Completed  :: {timeStop} and found {missing} missing songs.", logger)
            else:
                self.displayMessage(f"Completed  :: {timeStop} and database looks good.", logger)

    # -------------
    def displayMessage(self, message, logger=None):
        """   Display the message to screen and pass to logger if required.
              If a logger is passed in, then use it - else ignore.
        """
        print(message)
        if logger:
            logger.info(message)



