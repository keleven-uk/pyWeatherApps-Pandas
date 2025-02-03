###############################################################################################################
#    Records.py    Copyright (C) <2025>  <Kevin Scott>                                                 #
#                                                                                                             #
#    A class to hold the monthly records.                                                                     #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2025>  <Kevin Scott>                                                                      #
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

from src.classes.records import Records


class dailyRecords(Records):
    """  A class to hold the monthly weather records.

         All values should be numeric when passed in.

         Inherits from src.classes.records
    """

    def __init__(self):
        """  Set up class.
        """
        super().__init__()


    def show(self, reportValues, day, month, year):
        """  Prints to screen the contains of the records in a pretty table.

             Overrides the same method in the parent class.

             Supplies the custom title.
        """
        title = f" Weather Records for {day} {month} {year}"
        super().show(title, reportValues)
