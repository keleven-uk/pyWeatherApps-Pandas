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

import sys
import datetime

import pymsgbox

import pandas as pd
import src.projectPaths as pp
import src.classes.fileStore as fs
import src.classes.periodStore as ps
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

    def __init__(self, logger, config):
        self.logger    = logger
        self.config    = config
        self.fStore    = fs.FileStore(self.logger)            #  Create the file store.
        self.pStore    = ps.PeriodStore(self.logger)          #  Create the period store, holds year and month that contain data.
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

            #  re-sort the dataFrame in date order.
            utils.logPrint(self.logger, True, " Sorting the file data.", "info")
            self.dfData.sort_values(by="Date", ascending=True, inplace=True)

            #  Re-index the dataFrame, if not all the sperate files produces their own index.
            #  If you don't "drop" the index, it will add a new index, and save the old index values as a series in your dataframe
            utils.logPrint(self.logger, True, " Re-indexing the data store.", "info")
            self.dfData.reset_index(drop=True, inplace=True)
        else:
            utils.logPrint(self.logger, True, " No files to Process.", "info")


        utils.logPrint(self.logger, True, " Saving the file store.", "info")
        self.fStore.save()
        utils.logPrint(self.logger, True, " Saving the period store.", "info")
        self.pStore.save()
        utils.logPrint(self.logger, True, " Saving the data store.", "info")
        self.dfData.to_pickle(self.storeName)
        #print(self.dfData.tail())
        #self.dfData.to_csv("data.csv")
    #-------------------------------------------------------------------------------- checkData(self, checkDB) ------------------
    def info(self):
        """  Print our info about the data store [Pandas dataFrame]
        """
        print(f"\n Data runs from {self.config.START_DATE} to {self.config.END_DATE} and comprises {self.config.NO_OF_LINES} days \n")
        self.dfData.info(verbose=True)
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
        startDate    = self.strToDate(self.config.START_DATE)
        endDate      = self.strToDate(self.config.END_DATE)
        noOfLines    = self.config.NO_OF_LINES

        for fileName in self.fStore.storeFiles():
            fileData = self.fStore.getItem(fileName)

            if not fileData[0]:
                dataMonth = fileData[1]
                dataYear  = fileData[2]
                fileDate  = fileData[3]

                """  Two extra columns was added to the data on the 1ast July 2025.
                     The columns were "Heap" and "Run Time", these were added at the end of the table.

                     Then two extra columns were added on the 13th of July 2025.
                     The columns were "VPD" and "10-minute Average Wind Direction", these were added at columns 5 and 20.

                     Then three extra columns were added on the 15th 0f September 2025.
                     The columns were "Indoor Feels Like". "Indoor Dew Point", "Rainfall 24 Hours",
                     These were added at columns 8, 9 & 23 - these moved the above extra columns.
                """
                if fileDate >= datetime.datetime(2025, 7, 1) and fileDate < datetime.datetime(2025, 7, 13):
                    columnHeaders = pp.columnHeaders_1
                    rowsToSkip    = [0,23,24]
                elif fileDate > datetime.datetime(2025, 7, 12)and fileDate < datetime.datetime(2025, 9, 16):
                    columnHeaders = pp.columnHeaders_2
                    rowsToSkip    = [0,5,20,23,24]
                elif fileDate > datetime.datetime(2025, 9, 15):
                    columnHeaders = pp.columnHeaders_3
                    rowsToSkip    = [0,5,8,9,16,23,26,27]
                else:
                    columnHeaders = pp.columnHeaders
                    rowsToSkip    = [0]

                noOfLines += 1

                if CurrentYear != dataYear:
                    CurrentYear = dataYear
                    if not self.pStore.hasYear(CurrentYear):
                        self.pStore.addYear(dataYear)
                if currentMonth != dataMonth:
                    currentMonth = dataMonth
                    if not self.pStore.hasMonth(CurrentYear, dataMonth):
                        self.pStore.addMonth(dataYear, dataMonth)
                    utils.logPrint(self.logger, True, f" Processing new data files for {currentMonth} {CurrentYear}", "info")

                data = pd.read_excel(fileName, skiprows=rowsToSkip, na_values=[0.0], names=columnHeaders)

                #  This forces all entries to be of type float, all errors will be set to NaN.
                #  We ignore the first header "date", this is not numeric and will be sorted with later.
                data[pp.columnHeaders[1:]] = data[pp.columnHeaders[1:]].apply(pd.to_numeric, errors = "coerce")
                #  Then swap all NaN with zero.
                #  Thus makes further reporting easier.
                data[pp.columnHeaders[1:]] = data[pp.columnHeaders[1:]].fillna(0)

                # Overwriting date column after changing the Data to be of the format datetime from string.
                data["Date"] = pd.to_datetime(data["Date"])

                currDate  = data["Date"].iloc[0]

                if currDate < startDate:
                    startDate = currDate
                if currDate > endDate:
                    endDate = currDate

                #  Add the new cleaned dataframe to the main dataframe.
                self.dfData = self.dfData._append(data)

                self.fStore.setProcessed(fileName)                                              #  Mark files as processed.

        self.config.START_DATE  = startDate.strftime("%d-%m-%Y")
        self.config.END_DATE    = endDate.strftime("%d-%m-%Y")
        self.config.NO_OF_LINES = noOfLines

        self.config.writeConfig()
    #-------------------------------------------------------------------------------- __load(self) ------------
    def __load(self):
        """  Attempt to load the data store, if not create a new empty one.
        """
        try:
            self.dfData = pd.read_pickle(self.storeName)                #  Load data store, if it exists.
        except FileNotFoundError:
            self.dfData = pd.DataFrame()                                #  Create the data Pandas Dataframe.
    #-------------------------------------------------------------------------------- zap(self) ------------
    def zap(self):
        responce = pymsgbox.confirm(text="""Are you sure you want to clear the Data and File stores \
                                            You will need to build again.""", title="Warning", buttons=["OK", "Cancel"])

        if responce == "OK":
            utils.logPrint(self.logger, True, f" Deleting Data Store : {self.storeName}", "info")

            try:
                self.storeName.unlink()
            except FileNotFoundError:
                utils.logPrint(self.logger, True, f" Error deleting {self.storeName}", "warning")

            self.fStore.zap()       #  does it's own exception catching.'
            self.pStore.zap()       #  does it's own exception catching.'

    def strToDate(self, strDate):
        """  Converts a string to a datetime.
        """
        try:
            return datetime.datetime.strptime(strDate, "%d-%m-%Y")
        except ValueError as e:
            utils.logPrint(self.logger, True, f"ERROR :: {strDate} Cannot be converted to datetime {e}.", "danger")
            print("Goodbye.")
            sys.exit(3)


