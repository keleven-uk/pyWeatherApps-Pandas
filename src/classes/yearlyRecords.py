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


class yearlyRecords(Records):
    """  A class to hold the yearly weather records.

         All values should be numeric when passed in.

         Inherits from src.classes.records
    """
    def __init__(self, config):
        """  Set up class.
        """
        super().__init__()
        self.myConfig = config


    def show(self, reportValues, year):
        """  Prints to screen the contains of the records in a pretty table.

             Overrides the same method in the parent class.

             Supplies the custom title.
        """
        super().show(f" Weather Records for {year} for {self.myConfig.LOCATION}", reportValues)

        today     = datetime.now()
        yearStart = f"01-01-{year}"
        yearEnd   = f"31-12-{year}"

        if year == today.year:
            yearEnd = self.myConfig.END_DATE

        if self.myConfig.LOCATION == "All":
            if year == 2023:
                print("** only from July 2023 **")
                yearEnd   = "02-07-2023"
            elif year == 2024:
                print("** No data through 3 July 2024 - 22 October 2024 due to a faulty temperature sensor. **" )
            elif year == 2025:
                tmpEnd  = yearEnd
                yearEnd = self.myConfig.END_GILBERDYKE
            print(f"Data from {yearStart} to {yearEnd} collected at Gilberdyke, East Yorkshire")
            if year == 2025:
                yearStart = self.myConfig.START_HEDON
            print(f"Data from {yearStart} to {tmpEnd} collected at Hedon, East Yorkshire")
        elif self.myConfig.LOCATION == "Gilberdyke":
            if year == 2023:
                print("** only from July 2023 **")
            elif year == 2024:
                print("** No data through 3 July 2024 - 22 October 2024 due to a faulty temperature sensor. **" )
            print(f"Data runs from {yearStart} to {yearEnd}")
        elif self.myConfig.LOCATION == "Hedon":
            if year == 2025:
                yearStart = self.myConfig.START_HEDON
            print(f"Data runs from {yearStart} to {yearEnd}")

        print(f"Table generated {datetime.now().strftime("%d-%m-%Y  %H:%M")}")
