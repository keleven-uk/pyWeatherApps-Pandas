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

import pickle

import src.timer as timer
import src.projectPaths as pp
import src.Exceptions as myExceptions
import src.utils.dataUtils as utils

class FileStore():
    """  A simple class that wraps the file store dictionary.

         usage:
         self.fStore = fs.FileStore(path)
            path = path to location of the filestore

         to add an item              - self.fStore.addItem(key) - Data specific.
         to retrieve an item         - filedata = self.fStore.getItem(key) - Data specific.
         to test for key             - if self.fStore.hasKey(key):
         to return number of items   - l = self.fStore.noOfItems()
         to test database integrity  - self.fStore.check("test") - Data specific.
         to prune database           - self.fStore.check("delete")
         to load items               - self.fStore.load()
         to save items               - self.fStore.save()
         to return a list of keys    = self.fStore.storeFiles()

         TODO - possibly needs error checking [some done, some to go].
    """

    def __init__(self, logger):
        self.fileName = pp.DATA_PATH / "fileStore.pickle"
        self.logger   = logger
        self.timer    = timer.Timer()                #  A timer class.

        self.__load()

    #---------------------------------------------------------------------------------------------- __listFiles() -----------------------
    def checkNewFiles(self):
        """  Produce a list of weather data files in the data directory.
             Returns the number of the new files and a list of their file paths.
        """
        dataFiles = pp.DATA_PATH.rglob("*.xlsx")
        newFiles  = 0

        for file in dataFiles:
            if not self.hasKey(file):
                self.addItem(file)
                newFiles += 1

        return newFiles
    #---------------------------------------------------------------------------------------------- hasKey(self, key) -----------------------
    def hasKey(self, key):
        """  Returns true if the key exist in the fileStore.
        """
        return key in self.fileStore
    #---------------------------------------------------------------------------------------------- addItem(self, key, item1) -----------------
    def addItem(self, key):
        """  Adds to the fileStore, the key is a path.
             item1 is set to False, this indicates is has been added but not processed.
             item2 is set to the month of the file.
             item3 is set to the year of the file.
        """
        month = key.parts[8]
        year  = key.parts[7]
        self.fileStore[key] = [False, month, year]
    #---------------------------------------------------------------------------------------------- getItem(self, key) -----------------
    def getItem(self, key):
        """  Returns items at position key from the fileStore.
        """
        if self.hasKey(key):
            return self.fileStore[key]
        else:
            raise myExceptions.LibraryError
    #---------------------------------------------------------------------------------------------- getItem(self, key) -----------------
    def setProcessed(self, key):
        """  Mark item as processed.
        """
        if self.hasKey(key):
            self.fileStore[key][0] = True
        else:
            raise myExceptions.LibraryError
    #---------------------------------------------------------------------------------------------- getItem(self, key) -----------------
    def delItem(self, key):
        """  Deletes item at position key from the library.
        """
        try:
            del self.library[key]
        except (KeyError):
            raise myExceptions.LibraryError from None
    #---------------------------------------------------------------------------------------------- storeFiles(self) -----------------
    def storeFiles(self):
        """  Returns a list of the fileStore keys i.e. a list of the files in the store.
        """
        return self.fileStore.keys()
    #---------------------------------------------------------------------------------------------- noOfItems(self) -----------------
    @property
    def noOfItems(self):
        """  Return the number of entries in the fileStore
        """
        if not self.fileStore:
            self.load()
        return len(self.fileStore)
    #---------------------------------------------------------------------------------------------- save(self) -----------------------
    def save(self):
        """  Save the fileStore in pickle format - pickle format.
        """
        with open(self.fileName, "wb") as pickle_file:
            pickle.dump(self.fileStore, pickle_file)
    #---------------------------------------------------------------------------------------------- __load(self) -----------------------
    def __load(self):
        """  Loads the fileStore from disc - pickle format.
        """
        try:
            with open(self.fileName, "rb") as pickle_file:
                self.fileStore = pickle.load(pickle_file)
        except FileNotFoundError:
            utils.logPrint(self.logger, True, f"ERROR :: Cannot find library file. {self.fileName}.  Will use an empty library", "info")
            self.fileStore = {}
    #-------------------------------------------------------------------------------- check(self, mode, logger=None) -----------------------
    def check(self, mode, logger=None):
        """  Runs a database data integrity check.

             If a logger is passed in, then use it - else ignore.
        """
        self.timer.Start()        #  Start timer.
        missing   = 0
        removed   = 0

        if logger:
            logger.info("-" * 100)

        utils.logPrint(self.logger, True, f"Running database integrity check on {self.fileName} in {mode} mode", "info")
        utils.logPrint(self.logger, True, f"Loading {self.fileName}", "info")

        if not self.fileStore:
            try:
                self.load()
            except FileNotFoundError:
                raise myExceptions.LibraryError from None

        no_files = self.noOfItems
        utils.logPrint(self.logger, True, f"File Store has {no_files} files", "info")

        for filePath in self.fileStore.copy():  # iterate over a copy, gets around the error dictionary changed size during iteration
            path, month, year = self.getItem(filePath)
            if not filePath.exists():
                if mode == "delete":
                    self.delItem(filePath)
                    print(f"Deleting {filePath}")
                    removed += 1
                else:
                    missing += 1
                    print(f"File does not exist {filePath}")

        timeStop = self.timer.Stop      #  Stop timer.

        if removed:
            utils.logPrint(self.logger, True, f"Saving {self.fileName}", "info")
            self.save()
            utils.logPrint(self.logger, True, f"Completed  :: {timeStop} and removed {removed} entries from database.", "info")
            no_songs = self.noOfItems
            utils.logPrint(self.logger, True, f"File Store has now {no_songs} files", "info")
        else:
            if missing:
                utils.logPrint(self.logger, True, f"Completed  :: {timeStop} and found {missing} missing files.", "info")
            else:
                utils.logPrint(self.logger, True, f"Completed  :: {timeStop} and database looks good.", "info")
    #-------------------------------------------------------------------------------- zap(self) ------------
    def zap(self):
            utils.logPrint(self.logger, True, f" Deleting File Store {self.fileName}", "info")

            try:
                self.fileName.unlink()
            except FileNotFoundError:
                utils.logPrint(self.logger, True, f" Error deleting {self.fileName}", "warning")



