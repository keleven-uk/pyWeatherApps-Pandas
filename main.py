###############################################################################################################
#    main.py   Copyright (C) <2025>  <Kevin Scott>                                                            #
#                                                                                                             #
#    pyWeatherApp - Builds a main database out of individual daily spreadsheets.                              #
#                   The main database can be either a Excel spreadsheet or a SQLite3 database.                #
#                                                                                                             #
#  Usage:                                                                                                     #
#     main.py [-h] for help.                                                                                  #
#                                                                                                             #
#     For changes see history.txt                                                                             #
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


#  Data = 3 July 2023 - 22 October 2024 and 4 November - current.
#  The break is for a faulty temperature sensor.

import sys
import datetime

import src.args as args
import src.timer as Timer
import src.config as Config
import src.logger as Logger
import src.license as License
import src.projectPaths as pp

import src.classes.dataStore as ds
import src.classes.reports as rep
import src.classes.plotting as pl

import src.utils.dataUtils as utils

if __name__ == "__main__":

    utils.checkPaths(None, False)        #  Needs to be run first to ensure certain directories exist.
                                         #  None because there is no logger yet and True for verbose [to screen]

    Config = Config.Config(pp.CONFIG_PATH)                                 #  Need to do this first.
    logger = Logger.get_logger(str(pp.LOGGER_PATH))                        #  Create the logger.

    utils.logPrint(logger, False, "=" * 100, "info")

    License.printShortLicense(Config.NAME, Config.VERSION, logger)

    build, plot, info, checkDB, Areport, Yreport, Mreport, Dreport, reportYear, reportMonth, reportDay, Zap, reportMonthly = args.parseArgs(Config, logger)

    utils.logPrint(logger, True, f"Start of {Config.NAME} {Config.VERSION}", "info")

    timer = Timer.Timer()
    timer.Start()

    dataStore = ds.dataStore(logger, Config)
    reports   = rep.Reports()
    plots     = pl.Plots(Config)

    if checkDB:
        dataStore.checkData(checkDB)
    elif info:
        dataStore.info()
    elif build:
        dataStore.buildData()
    elif Areport:
        reports.allTimeReport()
        if plot:
            plots.allTimePlot(plot)
    elif Dreport:
        reports.dayReport(reportYear, reportMonth, reportDay)
        if plot:
            plots.dayPlot(reportYear, reportMonth, reportDay, plot)
    elif Mreport:
        reports.monthReport(reportYear, reportMonth)
        if plot:
            plots.monthPlot(reportYear, reportMonth, plot)
    elif Yreport:
        reports.yearReport(reportYear)
        if plot:
            plots.yearPlot(reportYear, plot)
    elif reportMonthly:
        reports.MonthlyReport(reportMonth)
    elif Zap:
        dataStore.zap()

        strNow  = datetime.datetime.now()
        written = strNow.strftime("%d-%m-%Y")
        Config.START_DATE  = f"{written}"                       #  reset to todays date, so an earlier date will be start
        Config.END_DATE    = ""
        Config.NO_OF_LINES = 0
        Config.writeConfig()
    else:
        utils.logPrint(logger, True, f"No arguments, please run {Config.NAME} -h", "danger")


    timeStop = timer.Stop

    print("")
    utils.logPrint(logger, True, f"{Config.NAME} Completed :: {timeStop}", "info")
    utils.logPrint(logger, True, f"End of {Config.NAME} {Config.VERSION}", "info")
    utils.logPrint(logger, False, "-" * 100, "info")

    sys.exit(0)
