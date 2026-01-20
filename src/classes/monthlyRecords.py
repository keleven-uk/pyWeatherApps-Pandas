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

    def __init__(self, config):
        """  Set up class.
        """
        super().__init__()
        self.myConfig = config


    def show(self, reportValues, month, year):
        """  Prints to screen the contains of the records in a pretty table.

             Overrides the same method in the parent class.

             Supplies the custom title.
        """

        if year:
            title = f" Weather Records for {month} {year} for {self.myConfig.LOCATION}"
        else:
            title = f" Weather Records for {month} across all years {reportValues["uniqueYears"]} for {self.myConfig.LOCATION}"
            del reportValues["uniqueYears"]             # not now needed, can upset the displayed table.

        super().show(title, reportValues)

        if year == 2025 and month == "July":
            if self.myConfig.LOCATION == "All":
                print(f"Data from 01-07-2025 to {self.myConfig.END_GILBERDYKE} collected at Gilberdyke, East Yorkshire")
                print(f"Data from {self.myConfig.START_HEDON} to 31/07/2025 collected at Hedon, East Yorkshire")
            elif self.myConfig.LOCATION == "Gilberdyke":
                print(f"Data from 01-07-2025 to {self.myConfig.END_GILBERDYKE} collected at Gilberdyke, East Yorkshire")
            elif self.myConfig.LOCATION == "Hedon":
                print(f"Data from {self.myConfig.START_HEDON} to 31/07/2025 collected at Hedon, East Yorkshire")
        if year == 2023 and month in ["July", "August", "September", "October"]:
            print("** No data through 3 July 2024 - 22 October 2024 due to a faulty temperature sensor. **" )

        print(f"Table generated {datetime.now().strftime("%d-%m-%Y  %H:%M")}")

