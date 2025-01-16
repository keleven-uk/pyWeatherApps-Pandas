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

from datetime import datetime

import src.projectPaths as pp
import src.classes.allTimeRecords as atr

class Reports():

    def __init__(self):
        self.DataStoreName = pp.DATA_PATH / "dataStore.pickle"
        self.reportValues  = {}
        self.__load()

    def allTimeReport(self):

        rep = atr.AllTimeRecords()

        for column in pp.columnHeaders:

            if column in ["Rain Yearly"]:
                continue

            maxDate = self.__convertDate(self.dfData[column].idxmax(), column)
            minDate = self.__convertDate(self.dfData[column].idxmin(), column)
            self.reportValues[f"{column}_max"] = (self.dfData[column].max(), maxDate)
            self.reportValues[f"{column}_min"] = (self.dfData[column].min(), minDate)

        rep.show(self.reportValues)

    #-------------------------------------------------------------------------------- __load(self) ---------------------------
    def __load(self):
        """  Attempt to load the data store, if not create a new empty one.
        """
        try:
            self.dfData = pd.read_pickle(self.DataStoreName)            #  Load data store, if it exists.
        except FileNotFoundError:
            self.dfData = pd.DataFrame()                                #  Create the data Pandas Dataframe.
    #-------------------------------------------------------------------------------- __convertDate(self, strDate) ------------
    def __convertDate(self, strDate, column):
        dateFormat = "%Y-%m-%d %H:%M"
        dateObj    = datetime.strptime(strDate, dateFormat)

        match column:
            case "Rain Monthly":
                month = dateObj.month
                year  = dateObj.year
                newDate = f"{calendar.month_name[month]} {year}"
            case "Rain Weekly":
                newDate = dateObj.strftime("%d-%m-%Y")
            case _:
                newDate = dateObj.strftime("%d-%m-%Y, %H:%M")

        return newDate

