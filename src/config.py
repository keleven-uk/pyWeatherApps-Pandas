###############################################################################################################
#    myConfig.py    Copyright (C) <2025>  <Kevin Scott>                                                       #
#                                                                                                             #
#    A class that acts has a wrapper around the configure file - config.toml.                                 #
#    The configure file is first read, then the properties are made available.                                #
#    The configure file is currently in toml format.                                                          #
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

import toml

from src.console import console


class Config():
    """  A class that acts has a wrapper around the configure file - config.toml.
         The configure file is hard coded and lives in the same directory has the main script.
         The configure file is first read, then the properties are made available.

         If config.toml is not found, a default configure file is generated.

         usage:
            myConfig = myConfig.Config()
    """

    FILE_NAME = "Config.toml"

    def __init__(self, CONFIG_PATH):

        self.FILE_NAME = CONFIG_PATH

        try:
            with open(self.FILE_NAME, "r") as configFile:       # In context manager.
                self.config = toml.load(configFile)             # Load the configure file, in toml.
        except FileNotFoundError:
            console.print("Configure file not found.", "warning")
            console.print("Writing default configure file.", "warning")
            console,print("Please check config values.", "warning")
            self._writeDefaultConfig()
            console.print("Running program with default configure settings.", "warning")
        except toml.TomlDecodeError:
            console.print("Configure file can't be read.", "warning")
            console.print("Writing default configure file.", "warning")
            console,print("Please check config values.", "warning")
            self._writeDefaultConfig()
            console.print("Running program with default configure settings.", "warning")

    @property
    def NAME(self):
        """  Returns application name.
        """
        return self.config["INFO"]["myNAME"]

    @property
    def VERSION(self):
        """  Returns application Version.
        """
        return self.config["INFO"]["myVERSION"]

    @property
    def REPORT_YEARS(self):
        reportYears = self.config["DATA"]["reportYears"]
        return f"{reportYears}"

    @property
    def MONTH(self):
        month = self.config["DATA"]["month"]
        return f"{month}"

    @property
    def YEAR(self):
        year = self.config["DATA"]["year"]
        return f"{year}"

    @property
    def GRAPH_WIDTH(self):
        graph_width = self.config["GRAPH"]["width"]
        return f"{graph_width}"

    @property
    def GRAPH_HEIGHT(self):
        graph_height = self.config["GRAPH"]["height"]
        return f"{graph_height}"

    @property
    def GRAPH_X_POS(self):
        xPos = self.config["GRAPH"]["X_pos"]
        return f"{xPos}"

    @property
    def GRAPH_Y_POS(self):
        yPos = self.config["GRAPH"]["Y_pos"]
        return f"{yPos}"

    @property
    def GRAPH_LINE_WIDTH(self):
        lineWidth = self.config["GRAPH"]["lineWidth"]
        return f"{lineWidth}"

    @property
    def GRAPH_LINE_STYLE(self):
        lineStyle = self.config["GRAPH"]["lineStyle"]
        return f"{lineStyle}"

    @property
    def GRAPH_LINE_COLOUR(self):
        lineStyle = self.config["GRAPH"]["lineColour"]
        return f"{lineStyle}"

    @property
    def GRAPH_ALPHA(self):
        lineColour = self.config["GRAPH"]["alpha"]
        return f"{lineColour}"

    @property
    def GRAPH_GRID(self):
        grid = self.config["GRAPH"]["grid"]
        return grid                                 #  Return Boolean.


    def _writeDefaultConfig(self):
        """ Write a default configure file.
            This is hard coded  ** TO KEEP UPDATED **
        """
        config = dict()

        config["INFO"] = {"myVERSION" : "2025.13",
                          "myNAME"    : "pyWeather"}

        config["DATA"] = {"reportYears" : ["2023", "2024", "2025"],
                          "month"       : "January",
                          "year"        : "2025"}

        config["GRAPH"] = {"width"      : 1400,
                           "height"     : 1000,
                           "X_pos"      : 40,
                           "Y_pos"      : 40,
                           "linewidth"  : 1,
                           "linestyle"  : "-",
                           "lineColour" : "blue",
                           "alpha"      : 0.75,
                           "grid"       : True}

        st_toml = toml.dumps(config)

        with open(self.FILE_NAME, "w") as configFile:       # In context manager.
            configFile.write("#   Configure files for pyDataBuild.py \n")
            configFile.write("#\n")
            configFile.write("#   true and false are lower case \n")
            configFile.write("#\n")
            configFile.write("#   <2025> (c) Kevin Scott \n")
            configFile.write("\n")
            configFile.writelines(st_toml)                  # Write configure file.

        with open(self.FILE_NAME, "r") as configFile:       # In context manager.
            self.config = toml.load(configFile)             # Load the configure file, in toml.
