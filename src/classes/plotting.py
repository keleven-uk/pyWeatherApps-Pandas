###############################################################################################################
#    plotting.py   Copyright (C) <2025>  <Kevin Scott>                                                        #
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

import matplotlib.pyplot as plt
import pandas as pd
import calendar

import src.projectPaths as pp

class Plots():

    def __init__(self):
        self.DataStoreName = pp.DATA_PATH / "dataStore.pickle"
        self.reportValues  = {}
        self.__load()
    #-------------------------------------------------------------------------------- allTimeReport(self) -----------------------
    def allTimePlot(self, colNumber):
        """  Produce a line graph from the all time data.
             The column is selected from the command line.
        """
        colName = self.__getColumnName(colNumber)

        fig = plt.figure()
        fig.canvas.manager.window.wm_geometry("1400x1000+20+20")

        plt.plot(self.dfData["Date"], self.dfData[f"{colName}"], linewidth="1", linestyle="-", alpha=0.5)

        plt.xlabel("Date")                              # add X-axis label
        plt.ylabel(colName)                             # add Y-axis label
        plt.title(f"All Time {colName}")                # add title

        # Display grid
        plt.grid(True)

        plt.show()                                      #  Show the graph.
    #-------------------------------------------------------------------------------- yearReport(self, reportYear) --------------
    def yearPlot(self, reportYear, colNumber):
        """  Process the data and extract the record values for a given year.
        """
        reportYear  = int(reportYear)
        colName     = self.__getColumnName(colNumber)

        dfYear = self.dfData[self.dfData["Date"].dt.year==reportYear]

        fig = plt.figure()
        fig.canvas.manager.window.wm_geometry("1400x1000+20+20")

        plt.plot(dfYear["Date"], dfYear[f"{colName}"], linewidth="1", linestyle="-", alpha=0.5)

        plt.xlabel("Date")                              # add X-axis label
        plt.ylabel(colName)                             # add Y-axis label
        plt.title(f"All Time {colName} for {reportYear}")                # add title

        # Display grid
        plt.grid(True)

        plt.show()
    #-------------------------------------------------------------------------------- yearReport(self, reportYear) --------------
    def monthPlot(self, reportYear, reportMonth, colNumber):
        """  Process the data and extract the record values for a given month and year.

             I had problems trying to extract the data between two dates.
             So, opted the easy option.  First I create a new dataFrame for the given year and
             then extract the required month from that.
        """
        reportYear  = int(reportYear)
        searchMonth = list(calendar.month_name).index(reportMonth)  #  Converts the month to a number for searching.
        colName     = self.__getColumnName(colNumber)

        dfYear  = self.dfData[self.dfData["Date"].dt.year==reportYear]
        dfMonth = dfYear[dfYear["Date"].dt.month==searchMonth]

        fig = plt.figure()
        fig.canvas.manager.window.wm_geometry("1400x1000+20+20")

        plt.plot(dfMonth["Date"], dfMonth[f"{colName}"], linewidth="1", linestyle="-", alpha=0.5)

        plt.xlabel("Date")                              # add X-axis label
        plt.ylabel(colName)                             # add Y-axis label
        plt.title(f"All Time {colName} for {reportMonth} {reportYear}")                # add title

        # Display grid
        plt.grid(True)

        plt.show()
    #-------------------------------------------------------------------------------- __load(self) ----------------------------------
    def __load(self):
        """  Attempt to load the data store, if not create a new empty one.
        """
        try:
            self.dfData = pd.read_pickle(self.DataStoreName)            #  Load data store, if it exists.
        except FileNotFoundError:
            self.dfData = pd.DataFrame()                                #  Create the data Pandas Dataframe.
    #-------------------------------------------------------------------------------- __getColumnName(self, number) ----------------------------------
    def __getColumnName(self, number):
        cols = ["Date", "Outdoor Temperature", "Outdoor Feels Like", "Outdoor Dew Point", "Outdoor Humidity",
        "Indoor Temperature", "Indoor Humidity", "Solar", "UVI", "Rain Rate", "Rain Daily",
        "Rain Event", "Rain Hourly", "Rain Weekly", "Rain Monthly", "Rain Yearly",
        "Wind Speed", "Wind Gust", "Wind Direction", "Pressure Relative", "Pressure Absolute"]

        return cols[number]

