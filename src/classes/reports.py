###############################################################################################################
#    reports.py   Copyright (C) <2025>  <Kevin Scott>                                                         #
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
import calendar

import src.projectPaths as pp
import src.classes.yearlyRecords as yr
import src.classes.allTimeRecords as atr

class Reports():

    def __init__(self):
        self.DataStoreName = pp.DATA_PATH / "dataStore.pickle"
        self.reportValues  = {}
        self.__load()
    #-------------------------------------------------------------------------------- allTimeReport(self) -----------------------
    def allTimeReport(self):
        """  Process the data and extract the all time record values.
        """
        rep = atr.AllTimeRecords()

        #  We ignore the first header "date", this is not numeric and will be sorted with later.
        for column in pp.columnHeaders[1:]:

            if column in ["Rain Yearly"]:
                continue

            maxVal  = self.dfData[column].max()
            maxPos  = self.dfData[column].idxmax()
            maxDate = self.dfData["Date"].iloc[maxPos]
            maxDate = self.__convertDate(maxDate, column)

            minVal  = self.dfData[column].min()
            minPos  = self.dfData[column].idxmin()
            minDate = self.dfData["Date"].iloc[minPos]
            minDate = self.__convertDate(minDate, column)

            self.reportValues[f"{column}_max"] = (maxDate, maxVal)
            self.reportValues[f"{column}_min"] = (minDate, minVal)

        rep.show(self.reportValues)
    #-------------------------------------------------------------------------------- yearReport(self, reportYear) --------------
    def yearReport(self, reportYear):
        """  Process the data and extract the record values for a given year.
        """
        reportYear = int(reportYear)
        rep = yr.yearlyRecords()

        for column in pp.columnHeaders[1:]:

            if column in ["Rain Yearly"]:
                continue

            maxVal  = self.dfData.groupby(self.dfData["Date"].dt.year==reportYear)[column].max()[True]
            maxPos  = self.dfData.groupby(self.dfData["Date"].dt.year==reportYear)[column].idxmax()[True]
            maxDate = self.dfData["Date"].iloc[maxPos]
            maxDate = self.__convertDate(maxDate, column)

            minVal  = self.dfData.groupby(self.dfData["Date"].dt.year==reportYear)[column].min()[True]
            minPos  = self.dfData.groupby(self.dfData["Date"].dt.year==reportYear)[column].idxmin()[True]
            minDate = self.dfData["Date"].iloc[minPos]
            minDate = self.__convertDate(minDate, column)

            self.reportValues[f"{column}_max"] = (maxDate, maxVal)
            self.reportValues[f"{column}_min"] = (minDate, minVal)

        rep.show(self.reportValues, year=reportYear)
#-------------------------------------------------------------------------------- __load(self) ----------------------------------
    def __load(self):
        """  Attempt to load the data store, if not create a new empty one.
        """
        try:
            self.dfData = pd.read_pickle(self.DataStoreName)            #  Load data store, if it exists.
        except FileNotFoundError:
            self.dfData = pd.DataFrame()                                #  Create the data Pandas Dataframe.
    #-------------------------------------------------------------------------------- __convertDate(self, strDate) ------------
    def __convertDate(self, strDate, column):
        """  Convert the date from Y-M-d to d-m-y.
             The input data is from Pandas dateTime - convert to string for processing.
             Strips out the day and time and returns the month name for Rain Monthly.
             Strips out the time for Rain Weekly.
             Returns a string.
        """
        newDate = strDate.strftime("%d-%m-%Y, %H:%M")

        match column:
            case "Rain Monthly":
                newDate = strDate.strftime("%d-%m-%Y, %H:%M")
                month = int(newDate[3:5])
                year  = int(newDate[6:10])
                newDate = f"{calendar.month_name[month]} {year}"
            case "Rain Weekly":
                newDate = newDate[0:10]

        return newDate

