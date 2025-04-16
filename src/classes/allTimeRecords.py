###############################################################################################################
#    allTimeRecords.py    Copyright (C) <2025>  <Kevin Scott>                                                 #
#                                                                                                             #
#    A class to hold the all time weather records.                                                            #
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


class AllTimeRecords(Records):
    """  A class to display the all time weather records.

         All values should be numeric when passed in.

         Inherits from src.classes.records
    """

    def __init__(self, config):
        """  Set up class.
        """
        super().__init__()
        self.myConfig = config


    def show(self, reportValues):
        """  Prints to screen the contains of the records in a pretty table.

             Overrides the same method in the parent class.

             reportValues - should hold a directory containing the data to display.
                The key should be the column header and data the value, date.

             Supplies the custom title.
        """
        super().show(f" All Time Weather Records {self.myConfig.START_DATE} - {self.myConfig.END_DATE}", reportValues)

        print(f"\n Data runs from {self.myConfig.START_DATE} to {self.myConfig.END_DATE} and comprises {self.myConfig.NO_OF_LINES} days")
        print("** No data through 3 July 2024 - 22 October 2024 due to a faulty temprature sensor. **" )
        print(f"Table generated {datetime.now().strftime("%d-%m-%Y  %H:%M")}")
