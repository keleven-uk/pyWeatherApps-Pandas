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
#    Copyright (C) <2023 - 2024>  <Kevin Scott>                                                               #
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

import src.args as args
import src.timer as Timer
import src.config as Config
import src.logger as Logger
import src.license as License
import src.projectPaths as pp
import src.classes.fileStore as fs

import src.utils.dataUtils as utils

if __name__ == "__main__":

    Config = Config.Config(pp.CONFIG_PATH)                                 #  Need to do this first.
    logger = Logger.get_logger(str(pp.LOGGER_PATH))                        #  Create the logger.
    fStore = fs.FileStore(pp.DATA_PATH)                                    #  Create the file store.

    utils.logPrint(logger, False, "=" * 100, "info")

    License.printShortLicense(Config.NAME, Config.VERSION, logger)

    utils.logPrint(logger, False, "-" * 100, "info")
    utils.logPrint(logger, True, f"Start of {Config.NAME} {Config.VERSION}", "info")

    args.parseArgs(Config, logger)


    timer = Timer.Timer()
    timer.Start()

    newFiles, filePaths = fStore.checkNewFiles()
    if newFiles != 0:
        utils.logPrint(logger, True, f" There are {newFiles} new data files", "info")
    else:
        utils.logPrint(logger, True, " No new data files found.", "info")

    fStore.save()


    timeStop = timer.Stop

    print("")
    utils.logPrint(logger, True, f"{Config.NAME} Completed :: {timeStop}", "info")
    utils.logPrint(logger, True, f"End of {Config.NAME} {Config.VERSION}", "info")
    utils.logPrint(logger, False, "-" * 100, "info")

    sys.exit(0)
