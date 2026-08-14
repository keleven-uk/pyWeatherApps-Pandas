###############################################################################################################
#    projectPaths.py   Copyright (C) <2025-26>  <Kevin Scott>                                                 #
#                                                                                                             #
#    Holds common directory paths for the project.                                                            #
#        Must sit in src directory                                                                            #
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

"""  A place to hold all the common project paths.
     Also, holds some common constants used in the project.
"""

import sys
import pathlib
import platformdirs as pp

appname   = "pyWeather"  #  Should be the same as in config.toml.
appauthor = "Keleven"

USER_DATA_DIR    = pathlib.Path(pp.user_data_dir(appname, appauthor))
USER_LOG_DIR     = pathlib.Path(pp.user_log_dir(appname, appauthor))
USER_RUNTIME_DIR = pathlib.Path(pp.user_runtime_dir(appname, appauthor))  #  if temp files are needed
PROJECT_PATH     = pathlib.Path(__file__).parent
MAIN_PATH        = pathlib.Path(__file__).parent.parent

#  If running as an executable i.e. from using auto-py-to-exe.
#  Some of the paths needs to be the working directory.
#  Except the log files, these will be somewhere like C:\Users\kevin\AppData\Local\Keleven\pyKlock\Logs

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    CONFIG_PATH   = USER_DATA_DIR / "config.toml"
    LOGGER_PATH   = USER_LOG_DIR  / f"{appname}.log"
    VERSION_PATH  = "version.toml"
    HISTORY_PATH  = "History.txt"
    LICENSE_PATH  = "LICENSE.txt"
    RESOURCE_PATH = "resources"
    HELP_PATH     = "help"
    DATA_PATH     = USER_DATA_DIR / "data"
else:
    CONFIG_PATH   = MAIN_PATH / "config.toml"
    LOGGER_PATH   = MAIN_PATH / f"logs/{appname}.log"
    VERSION_PATH  = MAIN_PATH / "docs/version.toml"
    HISTORY_PATH  = MAIN_PATH / "docs/History.txt"
    LICENSE_PATH  = MAIN_PATH / "LICENSE.txt"
    RESOURCE_PATH = MAIN_PATH / "resources"
    HELP_PATH     = MAIN_PATH / "help"
    DATA_PATH     = MAIN_PATH / "data"

#  Column headers for the Pandas dataframe.

"""  Two extra columns was added to the data on the 1ast July 2025.
        The columns were "Heap" and "Run Time", these were added at the end of the table.

        Then two extra columns where added on the 13th of July 2025.
        The columns were "VPD" and "10-minute Average Wind Direction", these were added at columns 5 and 20.

        Two columns, "Heap" and "Run Time",  where then removed 22 March 2026.
"""

#  21 Headers
columnHeaders = ["Date", "Outdoor Temperature", "Outdoor Feels Like", "Outdoor Dew Point", "Outdoor Humidity",
                 "Indoor Temperature", "Indoor Humidity", "Solar", "UVI", "Rain Rate", "Rain Daily",
                 "Rain Event", "Rain Hourly", "Rain Weekly", "Rain Monthly", "Rain Yearly",
                 "Wind Speed", "Wind Gust", "Wind Direction", "Pressure Relative", "Pressure Absolute"]

#  23 Headers
columnHeaders_1 = ["Date", "Outdoor Temperature", "Outdoor Feels Like", "Outdoor Dew Point", "Outdoor Humidity",
                 "Indoor Temperature", "Indoor Humidity", "Solar", "UVI", "Rain Rate", "Rain Daily","Rain Event",
                 "Rain Hourly", "Rain Weekly", "Rain Monthly", "Rain Yearly","Wind Speed", "Wind Gust",
                 "Wind Direction", "Pressure Relative", "Pressure Absolute", "Heap", "Run Time"]

#  25 Headers
columnHeaders_2 = ["Date", "Outdoor Temperature", "Outdoor Feels Like", "Outdoor Dew Point", "Outdoor Humidity", "VPD",
                 "Indoor Temperature", "Indoor Humidity", "Solar", "UVI", "Rain Rate", "Rain Daily","Rain Event",
                 "Rain Hourly", "Rain Weekly", "Rain Monthly", "Rain Yearly","Wind Speed", "Wind Gust",
                 "Wind Direction", "10-Minute", "Pressure Relative", "Pressure Absolute", "Heap", "Run Time"]

#  28 Headers
columnHeaders_3 = ["Date", "Outdoor Temperature", "Outdoor Feels Like", "Outdoor Dew Point", "Outdoor Humidity", "VPD",
                 "Indoor Temperature", "Indoor Humidity", "Indoor Feels Like", "Indoor Dew Point", "Solar", "UVI",
                 "Rain Rate", "Rain Daily","Rain Event", "Rain Hourly", "Rain 24 Hours","Rain Weekly", "Rain Monthly",
                 "Rain Yearly","Wind Speed", "Wind Gust", "Wind Direction", "10-Minute", "Pressure Relative",
                 "Pressure Absolute", "Heap", "Run Time"]

#  26 Headers
columnHeaders_4 = ["Date", "Outdoor Temperature", "Outdoor Feels Like", "Outdoor Dew Point", "Outdoor Humidity", "VPD",
                 "Indoor Temperature", "Indoor Humidity", "Indoor Feels Like", "Indoor Dew Point", "Solar", "UVI",
                 "Rain Rate", "Rain Daily","Rain Event", "Rain Hourly", "Rain 24 Hours","Rain Weekly", "Rain Monthly",
                 "Rain Yearly","Wind Speed", "Wind Gust", "Wind Direction", "10-Minute", "Pressure Relative",
                 "Pressure Absolute"]

#  36 Headers
columnHeaders_5 = ["Date", "Outdoor Temperature", "Outdoor Temperature Low", "Outdoor Temperature High", "Outdoor Feels Like", 
                 "Outdoor Dew Point", "Outdoor Humidity", "Outdoor Humidity Low", "Outdoor Humidity High", "VPD",
                 "Indoor Temperature", "Indoor Temperature Low", "Indoor Temperature High", "Indoor Humidity", "Indoor Humidity Low",
                 "Indoor Humidity High", "Indoor Feels Like", "Indoor Dew Point", "Solar", "UVI", "Rain Rate", "Rain Daily","Rain Event", 
                 "Rain Hourly", "Rain 24 Hours","Rain Weekly", "Rain Monthly", "Rain Yearly", "Wind Speed", "Wind Gust", "Wind Direction", 
                 "10-Minute", "Pressure Relative", "Pressure Relative Low", "Pressure Relative High", "Pressure Absolute"]
