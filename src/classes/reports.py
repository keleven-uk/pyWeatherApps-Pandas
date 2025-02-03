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
import src.classes.dailyRecords as dr
import src.classes.monthlyRecords as mr
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

            meanVal  = self.dfData[column].mean()

            self.reportValues[column] = (maxDate, maxVal, minDate, minVal, meanVal)

        rep.show(self.reportValues)
    #-------------------------------------------------------------------------------- yearReport(self, reportYear) --------------
    def yearReport(self, reportYear):
        """  Process the data and extract the record values for a given year.
        """
        reportYear = int(reportYear)

        rep = yr.yearlyRecords()

        dfYear = self.dfData[self.dfData["Date"].dt.year==reportYear]

        for column in pp.columnHeaders[1:]:

            if column in ["Rain Yearly"]:
                continue

            #  Re-index the dataFrame, if not all the sperate files produces their own index.
            #  If you don't "drop" the index, it will add a new index, and save the old index values as a series in your dataframe
            dfYear.reset_index(drop=True, inplace=True)

            maxVal  = dfYear[column].max()
            maxPos  = dfYear[column].idxmax()
            maxDate = dfYear["Date"].iloc[maxPos]
            maxDate = self.__convertDate(maxDate, column)

            minVal  = dfYear[column].min()
            minPos  = dfYear[column].idxmin()
            minDate = dfYear["Date"].iloc[minPos]
            minDate = self.__convertDate(minDate, column)

            meanVal  = dfYear[column].mean()

            self.reportValues[column] = (maxDate, maxVal, minDate, minVal, meanVal)

        rep.show(self.reportValues, year=reportYear)

    #-------------------------------------------------------------------------------- monthReport(self, reportYear, reportMonth) --------------
    def monthReport(self, reportYear, reportMonth):
        """  Process the data and extract the record values for a given month and year.

             I had problems trying to extract the data between two dates.
             So, opted the easy option.  First I create a new dataFrame for the given year and
             then extract the required month from that.
        """
        reportYear  = int(reportYear)
        searchMonth = list(calendar.month_name).index(reportMonth)  #  Converts the month to a number for searching.

        rep = mr.monthlyRecords()

        dfYear  = self.dfData[self.dfData["Date"].dt.year==reportYear]
        dfMonth = dfYear[dfYear["Date"].dt.month==searchMonth]

        for column in pp.columnHeaders[1:]:

            if column in ["Rain Yearly"]:
                continue

            #  Re-index the dataFrame, if not all the sperate files produces their own index.
            #  If you don't "drop" the index, it will add a new index, and save the old index values as a series in your dataframe
            dfMonth.reset_index(drop=True, inplace=True)

            maxVal  = dfMonth[column].max()
            maxPos  = dfMonth[column].idxmax()
            maxDate = dfMonth["Date"].iloc[maxPos]
            maxDate = self.__convertDate(maxDate, column)

            minVal  = dfMonth[column].min()
            minPos  = dfMonth[column].idxmin()
            minDate = dfMonth["Date"].iloc[minPos]
            minDate = self.__convertDate(minDate, column)

            meanVal = dfMonth[column].mean()

            self.reportValues[column] = (maxDate, maxVal, minDate, minVal, meanVal)

        rep.show(self.reportValues, month=reportMonth, year=reportYear)
    #-------------------------------------------------------------------------------- dayReport(self, reportYear, reportMonth, reportDay) --------------
    def dayReport(self, reportYear, reportMonth, reportDay):

        reportYear  = int(reportYear)
        searchMonth = list(calendar.month_name).index(reportMonth)  #  Converts the month to a number for searching.
        searchDay   = reportDay

        rep = dr.dailyRecords()

        dfYear  = self.dfData[self.dfData["Date"].dt.year==reportYear]
        dfMonth = dfYear[dfYear["Date"].dt.month==searchMonth]
        dfDay   = dfMonth[dfMonth["Date"].dt.day==searchDay]

        print(reportYear, reportMonth, reportDay)
        print(dfDay.info())

        for column in pp.columnHeaders[1:]:

            if column in ["Rain Yearly"]:
                continue

            #  Re-index the dataFrame, if not all the sperate files produces their own index.
            #  If you don't "drop" the index, it will add a new index, and save the old index values as a series in your dataframe
            dfDay.reset_index(drop=True, inplace=True)

            maxVal  = dfDay[column].max()
            maxPos  = dfDay[column].idxmax()
            maxDate = dfDay["Date"].iloc[maxPos]
            maxDate = self.__convertDate(maxDate, column)

            minVal  = dfDay[column].min()
            minPos  = dfDay[column].idxmin()
            minDate = dfDay["Date"].iloc[minPos]
            minDate = self.__convertDate(minDate, column)

            meanVal = dfDay[column].mean()

            self.reportValues[column] = (maxDate, maxVal, minDate, minVal, meanVal)

        rep.show(self.reportValues, day=reportDay, month=reportMonth, year=reportYear)
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

