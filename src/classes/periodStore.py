###############################################################################################################
#    periodStore.py   Copyright (C) <2025>  <Kevin Scott>                                                     #
#                                                                                                             #
#    A simple class that wraps the period store dictionary.                                                   #
#    The items to store are years,                                                                            #
#      The key is either made up of a list of the months                                                      #
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
import src.utils.dataUtils as utils

class PeriodStore():
    """  A simple class that wraps the period store dictionary.

         The store holds year and month that contain data.

         Mainly used to check command line arguments for month and year.

    """

    def __init__(self, logger):
        self.fileName = pp.DATA_PATH / "periodStore.pickle"
        self.logger   = logger
        self.timer    = timer.Timer()                #  A timer class.

        self.__load()

    #---------------------------------------------------------------------------------------------- hasYear(self, year) -----------------------
    def hasYear(self, year):
        """  Returns true if the key exist in the periodStore.
        """
        return year in self.periodStore
    #---------------------------------------------------------------------------------------------- hasMonth(self, year, month) -----------------------
    def hasMonth(self, year, month):
        """  Returns true if the key exist in the periodStore.
        """
        months = self.periodStore[year]
        return month in months
    #---------------------------------------------------------------------------------------------- addYear(self, year) -----------------
    def addYear(self, year):
        """  Adds to the periodStore, the key is the year.
        """

        self.periodStore[year] = []
    #---------------------------------------------------------------------------------------------- addMonth(self, year, month) -----------------
    def addMonth(self, year, month):
        """  Adds to the periodStore, the key is the year.
        """
        months = self.periodStore[year]
        months.append(month)
        self.periodStore[year] = months
    #---------------------------------------------------------------------------------------------- listYears(self) -----------------
    def listYears(self):
        """  Return a list of the years in the periodStore [keys].
        """
        return list(self.periodStore.keys())
    #---------------------------------------------------------------------------------------------- noOfItems(self) -----------------
    @property
    def noOfItems(self):
        """  Return the number of entries in the periodStore
        """
        if not self.periodStore:
            self.load()
        return len(self.periodStore)
    #---------------------------------------------------------------------------------------------- save(self) -----------------------
    def save(self):
        """  Save the periodStore in pickle format - pickle format.
        """
        with open(self.fileName, "wb") as pickle_file:
            pickle.dump(self.periodStore, pickle_file)
    #---------------------------------------------------------------------------------------------- __load(self) -----------------------
    def __load(self):
        """  Loads the periodStore from disc - pickle format.
        """
        try:
            with open(self.fileName, "rb") as pickle_file:
                self.periodStore = pickle.load(pickle_file)
        except FileNotFoundError:
            utils.logPrint(self.logger, True, f"ERROR :: Cannot find Period Store file. {self.fileName}.  Will use an empty Store", "info")
            self.periodStore = {}
        #-------------------------------------------------------------------------------- zap(self) ------------
    def zap(self):
            utils.logPrint(self.logger, True, f" Deleting File Store {self.fileName}", "info")

            try:
                self.fileName.unlink()
            except FileNotFoundError:
                utils.logPrint(self.logger, True, f" Error deleting {self.fileName}", "warning")
