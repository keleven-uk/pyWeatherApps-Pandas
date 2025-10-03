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

from datetime import datetime

from src.classes.records import Records


class monthlyRecords(Records):
    """  A class to hold the monthly weather records.

         All values should be numeric when passed in.

         Inherits from src.classes.records
    """

    def __init__(self):
        """  Set up class.
        """
        super().__init__()


    def show(self, reportValues, month, year):
        """  Prints to screen the contains of the records in a pretty table.

             Overrides the same method in the parent class.

             Supplies the custom title.
        """

        if year:
            title = f" Weather Records for {month} {year}"
        else:
            title = f" Weather Records for {month} across all years {reportValues["uniqueYears"]}"
            del reportValues["uniqueYears"]             # not new needed, can upset the displayed table.

        super().show(title, reportValues)

        if year == 2025 and month == "July":
            print("Data from 01-07-2025 to 15-07-2025 collected at Gilberdyke, East Yorkshire")
            print("Data from 17-07-2025 to 31/07/2025 collected at Hedon, East Yorkshire")

        if not year and month == "July":
            print("Data from 01-07-2025 to 15-07-2025 collected at Gilberdyke, East Yorkshire")
            print("Data from 17-07-2025 to 31/07/2025 collected at Hedon, East Yorkshire")

        print(f"Table generated {datetime.now().strftime("%d-%m-%Y  %H:%M")}")

