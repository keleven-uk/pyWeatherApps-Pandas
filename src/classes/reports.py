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
import src.utils.weatherUtils as utils

class Reports():

    def __init__(self, config):
        self.myConfig      = config
        self.DataStoreName = pp.DATA_PATH / "dataStore.pickle"
        self.reportValues  = {}
        self.__load()
        pd.options.mode.copy_on_write = True    # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    #-------------------------------------------------------------------------------- allTimeReport(self) -----------------------
    def allTimeReport(self):
        """  Process the data and extract the all time record values.
        """
        rep = atr.AllTimeRecords(self.myConfig)

        uniqueYears = (self.dfData["Date"].dt.year.unique())
        minYrRain   = 9999
        maxYrRain   = 0
        sumYrRain   = 0
        countYrRain = 0
        minMnRain   = 9999
        maxMnRain   = 0
        sumMnRain   = 0
        countMnRain = 0

        #  Loop through each year and sum the rain fall.
        #  There is a bug in the Ecowitt software, the yearly rain fall is not reset at new year.

        for year in uniqueYears:
            dfYear = self.dfData[self.dfData["Date"].dt.year==year]

            rainYrSum = utils.rainAmount(dfYear)

            sumYrRain   += rainYrSum
            countYrRain += 1

            if rainYrSum < minYrRain:
                minYrRain = rainYrSum
                minYrYear = year
            if rainYrSum > maxYrRain:
                maxYrRain = rainYrSum
                maxYrYear = year

            uniqueMonths = (dfYear["Date"].dt.month.unique())

            for month in uniqueMonths:
                dfMonth   = dfYear.loc[dfYear["Date"].dt.month==month]       # .loc is used to stop Boolean Series warnings.
                lastRow   = dfMonth.iloc[-1]
                rainDate  = self.__convertDate(lastRow["Date"], "Rain Monthly")
                rainValue = lastRow["Rain_Monthly"]

                sumMnRain   += rainValue
                countMnRain += 1

                if rainValue < minMnRain:
                    minMnRain = rainValue
                    minMnDate = f"{calendar.month_name[month]} {year}"
                if rainValue > maxMnRain:
                    maxMnRain = rainValue
                    maxMnDate = f"{calendar.month_name[month]} {year}"

        meanYr = sumYrRain / countYrRain
        meanMn = sumMnRain / countMnRain

        self.__getValues(self.dfData, "allTime")
        self.reportValues["Rain Monthly"] = (maxMnDate, maxMnRain, minMnDate, minMnRain, meanMn)
        self.reportValues["Rain Yearly"]  = (maxYrYear, maxYrRain, minYrYear, minYrRain, meanYr)
        rep.show(self.reportValues)
    #-------------------------------------------------------------------------------- yearReport(self, reportYear) --------------
    def yearReport(self, reportYear):
        """  Process the data and extract the record values for a given year.
        """
        minMnRain   = 9999
        maxMnRain   = 0
        sumMnRain   = 0
        countMnRain = 0

        reportYear = int(reportYear)

        rep = yr.yearlyRecords()

        dfYear = self.dfData[self.dfData["Date"].dt.year==reportYear]

        uniqueMonths = (dfYear["Date"].dt.month.unique())

        for month in uniqueMonths:
            dfMonth   = dfYear.loc[dfYear["Date"].dt.month==month]       # .loc is used to stop Boolean Series warnings.
            lastRow   = dfMonth.iloc[-1]
            rainDate  = self.__convertDate(lastRow["Date"], "Rain Monthly")
            rainValue = lastRow["Rain Monthly"]

            sumMnRain   += rainValue
            countMnRain += 1

            if rainValue < minMnRain:
                minMnRain = rainValue
                minMnDate = f"{calendar.month_name[month]} {reportYear}"
            if rainValue > maxMnRain:
                maxMnRain = rainValue
                maxMnDate = f"{calendar.month_name[month]} {reportYear}"

        meanMn = sumMnRain / countMnRain

        self.__getValues(dfYear, "Year")
        rainSum = utils.rainAmount(dfYear)                              #  Obtain the yearly rainfall.
        self.reportValues["Rain Monthly"] = (maxMnDate, maxMnRain, minMnDate, minMnRain, meanMn)
        self.reportValues["Rain Yearly"] = (reportYear, rainSum)
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

        self.__getValues(dfMonth, "Month")

        rep.show(self.reportValues, month=reportMonth, year=reportYear)
    #-------------------------------------------------------------------------------- MonthlyReport(self, reportMonth) --------------
    def MonthlyReport(self, reportMonth):
        """  Process the data and extract the record values for a given month across all years.
        """

        searchMonth = list(calendar.month_name).index(reportMonth)  #  Converts the month to a number for searching.

        rep = mr.monthlyRecords()

        dfMonth = self.dfData[self.dfData["Date"].dt.month==searchMonth]

        self.reportValues["uniqueYears"] = (dfMonth["Date"].dt.year.unique())

        self.__getValues(dfMonth, "Monthly")

        rep.show(self.reportValues, month=reportMonth, year=0)
    #-------------------------------------------------------------------------------- dayReport(self, reportYear, reportMonth, reportDay) --------------
    def dayReport(self, reportYear, reportMonth, reportDay):
        """  Process the data and extract the record values for a given day, month and year.
        """

        reportYear  = int(reportYear)
        searchMonth = list(calendar.month_name).index(reportMonth)  #  Converts the month to a number for searching.
        searchDay   = int(reportDay)

        rep = dr.dailyRecords()

        dfYear  = self.dfData[self.dfData["Date"].dt.year==reportYear]
        dfMonth = dfYear[dfYear["Date"].dt.month==searchMonth]
        dfDay   = dfMonth[dfMonth["Date"].dt.day==searchDay]

        self.__getValues(dfDay, "Day")

        rep.show(self.reportValues, day=reportDay, month=reportMonth, year=reportYear)
    #-------------------------------------------------------------------------------- __getValues(self, dfdata) ---------------------
    def __getValues(self, dfData, type):
        """  Extract the record values from a given dataFrame.
             The dataFrame should already been filtered for year, period etc.
        """
        #  Re-index the dataFrame, if not all the sperate files produces their own index.
        #  If you don't "drop" the index, it will add a new index, and save the old index values as a series in your dataframe
        dfData.reset_index(drop=True, inplace=True)

        #  We ignore the first header "date", this is not numeric and will be sorted with later.
        for column in pp.columnHeaders[1:]:

            if column in ["Rain Yearly"]:           #  Yearly rainfall is only used in all time and year reports.
                if type in ["allTime", "Year"]:
                    self.reportValues[column] = ()
                continue

            maxVal  = dfData[column].max()
            maxPos  = dfData[column].idxmax()
            maxDate = dfData["Date"].iloc[maxPos]
            maxDate = self.__convertDate(maxDate, column)

            minVal  = dfData[column].min()
            minPos  = dfData[column].idxmin()
            minDate = dfData["Date"].iloc[minPos]
            minDate = self.__convertDate(minDate, column)

            meanVal  = dfData[column].mean()

            if type in ["Month"] and column in ["Rain Monthly"]:
                self.reportValues[column] = (maxDate, maxVal)
            else:
                self.reportValues[column] = (maxDate, maxVal, minDate, minVal, meanVal)

        if type in ["allTime", "Year", "Month", "Monthly"]:
            rainDate, rainVal, droughtDate, droughtVal = utils.hoursRain(dfData)
            self.reportValues["Hour"] = (rainDate, rainVal, droughtDate, droughtVal)

            rainDate, rainVal, droughtDate, droughtVal   = utils.daysRain(dfData)
            self.reportValues["Days"] = (rainDate, rainVal, droughtDate, droughtVal)

            sunDate, sunVal, dullDate, dullVal, totalSun, totalDull = utils.daysSunshine(dfData)
            self.reportValues["Sun Consecutive"] = (sunDate, sunVal, dullDate, dullVal)
            self.reportValues["Sun Total"] = (totalSun, totalDull)
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

