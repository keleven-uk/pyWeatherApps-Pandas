###############################################################################################################
#    dataStore.py   Copyright (C) <2025>  <Kevin Scott>                                                       #
#                                                                                                             #
#                                                                                                             #
###############################################################################################################
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

import pandas as pd
import src.projectPaths as pp
import src.classes.fileStore as fs

import src.utils.dataUtils as utils


class dataStore():
    """  A simple class that wraps the date processing.

        usage:
        dataStore = ds.dataStore(logger)
        logger = link to the app logger.

    to build the data = dataStore.buildData.
    to check the data = dateStore.checkData.

        TODO - possibly needs error checking [some done, some to go].
    """

    def __init__(self, logger):
        self.fStore    = fs.FileStore()            #  Create the file store.
        self.logger    = logger
        self.storeName = pp.DATA_PATH / "dataStore.pickle"

        self.__load()
    #-------------------------------------------------------------------------------- buildData(self) ---------------------------
    def buildData(self):
        """  Calls the fileStore to scan for any new data file.
             Reports the number and saves the new fileStore.
        """
        newFiles = self.fStore.checkNewFiles()

        if newFiles != 0:
            utils.logPrint(self.logger, True, f" There are {newFiles} new data files", "info")
        else:
            utils.logPrint(self.logger, True, " No new data files found.", "info")

        newData = self.__anyNewData()
        if newData > 0:
            utils.logPrint(self.logger, True, f" There are {newData} new data files to process", "info")
            self.__processData()
        else:
            utils.logPrint(self.logger, True, " No files to Process.", "info")

        utils.logPrint(self.logger, True, " Saving the file store.", "info")
        self.fStore.save()
        utils.logPrint(self.logger, True, " Saving the data store.", "info")
        self.dfData.to_pickle(self.storeName)
    #-------------------------------------------------------------------------------- checkData(self, checkDB) ------------------
    def checkData(self, checkDB):
        """  Preforms an integrity check on the fileStore.
        """
        if checkDB == 1:
            self.fStore.check("test", self.logger)
        elif checkDB == 2:
            self.fStore.check("delete", self.logger)
            self.fStore.save()
    #-------------------------------------------------------------------------------- __anyNewData(self, fileList) ------------
    def __anyNewData(self):
        """  Scans the fileStore for any unprocessed files.
             When a file is added, the first data item is set to False - set to True when processed.
        """
        newData = 0
        for file in self.fStore.storeFiles():
            fileData = self.fStore.getItem(file)
            if not fileData[0]:
                newData += 1

        return newData
    #-------------------------------------------------------------------------------- __processData(self, fileList) ------------
    def __processData(self):
        """  Performs the actual processing of the new files - the Pandas stuff.
             Monitors for changing years and months, these make up part of the directory structure.
        """
        utils.logPrint(self.logger, True, " Processing new data files", "info")

        currentMonth = ""
        CurrentYear  = ""

        for fileName in self.fStore.storeFiles():
            fileData = self.fStore.getItem(fileName)
            if not fileData[0]:
                month = fileData[1]
                year  = fileData[2]

                if CurrentYear != year:
                    CurrentYear = year
                if currentMonth != month:
                    currentMonth = month
                    utils.logPrint(self.logger, True, f" Processing new data files for {currentMonth} {CurrentYear}", "info")

                data = pd.read_excel(fileName, skiprows=[0], index_col=0, na_values=[0.0], names=pp.columnHeaders)

                data_numeric = data.apply(pd.to_numeric, errors = "coerce")                     #  This forces all entries to be of type float,
                                                                                                #  all errors will be set to NaN.
                isAllNumeric = not data_numeric.isnull().values.any()                           #  Check if not now all numeric.
                if isAllNumeric:
                    print(f"Not all numeric {fileName}")

                self.dfData = self.dfData._append(data_numeric)

                self.fStore.setProcessed(fileName)                                              #  Mark files as processed.
    #-------------------------------------------------------------------------------- __load(self) ------------
    def __load(self):
        """  Attempt to load the data store, if not create a new empty one.
        """
        try:
            self.dfData = pd.read_pickle(self.storeName)                #  Load data store, if it exists.
        except FileNotFoundError:
            self.dfData = pd.DataFrame()                                #  Create the data Pandas Dataframe.



