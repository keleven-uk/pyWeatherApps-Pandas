###############################################################################################################
#    dataUtils.py   Copyright (C) <2025>  <Kevin Scott>                                                       #                                                                                                             #                                                                                                             #
#    A number of helper and utility functions                                                                 #
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

import os
import glob

from src.console import console

import src.projectPaths as pp

######################################################################################## loadExplorer() ######
def loadExplorer(logger):
    """  Load program working directory into file explorer.
    """
    try:
        os.startfile(os.getcwd(), "explore")
    except NotImplementedError as error:
        logger.error(error)

########################################################################################### logPrint() #######
def logPrint(logger, verbose, message, style):
    """  If a logger is supplied, log message.
         If screen is True, print message to screen.
    """
    if logger:
        logger.info(message)

    if verbose:
        if style == "warning":
            console.log(f"{message}", style="danger")
        elif style == "danger":
            console.log(f"{message}", style="warning")
        else:
            console.log(f"{message}", style="info")

########################################################################################### listFiles() ######
def listFiles(targetFiles, verbose):
    """  Produce a list of weather data files in the data directory.
         If screen is True [default], the file name will be printed to screen.

         NB  assumes it's run in the parent directory and the data files are in sub directory called data.'
    """
    dataFiles = glob.glob(targetFiles)

    if verbose:
        for file in dataFiles:
            console.log(f"Found data file :: {file}", style="info")

    return(dataFiles)

########################################################################################### checkPaths() #########
def checkPaths(logger, verbose):
    """  Checks the data directories exist, if not create them.
    """
    logPrint(logger, verbose, "Checking Paths", "info")

    dataPath = pp.DATA_PATH
    logPath  = pp.LOGGER_PATH.parent

    if dataPath.exists():
        logPrint(logger, verbose, f"{dataPath} exists", "info")
    else:
        logPrint(logger, verbose, f"{dataPath} doesn't exists, will create", "warning")
        dataPath.mkdir(parents=True)

    if logPath.exists():
        logPrint(logger, verbose, f"{logPath} exists", "info")
    else:
        logPrint(logger, verbose, f"{logPath} doesn't exists, will create", "warning")
        logPath.mkdir(parents=True)











