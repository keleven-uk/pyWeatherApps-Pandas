#############################################################################################################################
#    arguments.py   Copyright (C) <2025>  <Kevin Scott>                                                                     #
#                                                                                                                           #
#    A dataclass to hold the command line arguments.                       .                                                #
#                                                                                                                           #
#############################################################################################################################
#                                                                                                                           #
#    This program is free software: you can redistribute it and/or modify it under the terms of the                         #
#    GNU General Public License as published by the Free Software Foundation, either Version 3 of the                       #
#    License, or (at your option) any later Version.                                                                        #
#                                                                                                                           #
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without                      #
#    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                             #
#    GNU General Public License for more details.                                                                           #
#                                                                                                                           #
#    You should have received a copy of the GNU General Public License along with this program.                             #
#    If not, see <http://www.gnu.org/licenses/>.                                                                            #
#                                                                                                                           #
#############################################################################################################################

from dataclasses import dataclass

@dataclass
class Arguments:
    plot     : bool = False
    plotHelp : bool = False
    version  : bool = False
    license  : bool = False
    explorer : bool = False
    info     : bool = False
    checkDB  : int  = 0
    build    : bool = False
    location : str  = "ALL"
    year     : int  = 0
    month    : str  = ""
    day      : int  = 0
    Areport  : bool = False
    Yreport  : bool = False
    Dreport  : bool = False
    Mreport  : bool = False
    Treport  : bool = False
    Zap      : bool = False     # Capital Z - could be dangerous.

