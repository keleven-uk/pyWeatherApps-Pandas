###############################################################################################################
#    Records.py    Copyright (C) <2025>  <Kevin Scott>                                                        #
#                                                                                                             #
#    A class to hold records, this then subclassed to monthly, yearly and all time.                           #
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

from src.console import console, Table

class Records:
    """  A class to display weather records.

         All values should be numeric when passed in.

         usage:
                class r (Records):

                then
                    __init__()                #  Record files is a files for the records.
                        super().__init__()

                then call to

                r.show(title, reportValues)   #  To display the records in a pretty table.
    """

    def __init__(self):
        """  Set up class.
        """
    #-------------------------------------------------------------------------------- show(self, title, reportValues) ---------------------------
    def show(self, title, reportValues):
        """  Prints to screen the contains of the records in a pretty table.

             reportValues - should hold a directory containing the data to display.
                            The key should be the column header and data the value, date.

             The title of the table needs to be passed in.
        """
        Table.title = title

        Table.add_column("Category", justify="right", style="cyan", no_wrap=True)
        Table.add_column("Date", style="magenta")
        Table.add_column("Max Value", justify="left", style="green")
        Table.add_column("Date", style="magenta")
        Table.add_column("Min Value", justify="left", style="green")
        Table.add_column("Mean Value", justify="left", style="green")

        for key in reportValues:

            data      = reportValues[key]
            category  = key

            if category in ["Wind Direction"]:
                continue

            maxDate   = data[0]
            maxAmount = self.formatValue(category, data[1])

            if category in ["Solar", "UVI", "Rain Rate", "Rain Daily", "Rain Event", "Rain Hourly", "Rain Weekly", "Rain Monthly",
                            "Rain Yearly", "Wind Speed", "Wind Gust"]:
                minDate    = ""
                minAmount  = ""
            else:
                minDate    = data[2]
                minAmount  = self.formatValue(category, data[3])

            if category in ["Solar", "UVI", "Rain Rate", "Rain Daily", "Rain Event", "Rain Hourly",
                            "Rain Yearly", "Wind Speed", "Wind Gust", "Days", "Hour", "Sun"]:
                meanAmount = ""
            else:
                meanAmount = self.formatValue(category, data[4])

            if category == "Days":
                category  = "Consecutive Days of Rain/Drought"
                maxAmount = maxAmount + " Wet days"
                minAmount = minAmount + " Dry days"
                print(maxDate, minDate)
            if category == "Hour":
                category  = "Consecutive Hours of Rain/Drought"
                maxAmount = maxAmount + " Wet hours"
                minAmount = minAmount + " Dry hours"
            if category == "Sun":
                category  = "Consecutive Days of Sun/No Sun"
                maxAmount = maxAmount + " Sunny days"
                minAmount = minAmount + " Dull days"

            #  Add horizontal lines to the table to split the categories
            match category:
                case "Outdoor Humidity" | "Indoor Humidity" | "UVI" | "Rain Monthly" | "Wind Gust" | "Pressure Absolute":
                    Table.add_row(f"{category}", f"{maxDate}", f"{maxAmount}", f"{minDate}", f"{minAmount}", f"{meanAmount}", end_section=True)
                case _:
                    Table.add_row(f"{category}", f"{maxDate}", f"{maxAmount}", f"{minDate}", f"{minAmount}", f"{meanAmount}",)

        console.print(Table)

        print(f"Table generated {datetime.now().strftime("%d-%m-%Y  %H:%M")}")
    #-------------------------------------------------------------------------------- formatDate(self, category, amount) ---------------------------
    def formatValue(self, category, amount):
        """  Format values correctly and add imperial equivalents, if appropriate.
        """
        match category:
            case category if "Temperature" in category:
                value  = f"{amount:.2f}\N{DEGREE SIGN}C"
            case category if "Dew Point" in category:
                value  = f"{amount:.2f}\N{DEGREE SIGN}C"
            case category if "Feels Like" in category:
                value  = f"{amount:.2f}\N{DEGREE SIGN}C"
            case category if category.startswith("Rain"):
                value  = f"{amount:4.0f}mm ({amount*0.0393701:4.2f}in)"
            case category if category.startswith("Wind"):
                value  = f"{amount:.2f} km/h ({amount*0.6213715277778:.2f}mph)"
            case category if category.startswith("Solar"):
                value  = f"{amount} Klux"
            case category if category.startswith("Pressure"):
                value  = f"{amount:4.0f} hPa"
            case category if "Humidity" in category:
                value  = f"{amount:.2f}%"
            case category if "Days" in category:
                value  = f"{amount:4.0f}"
            case category if "Hour" in category:
                value  = f"{amount:4.0f}"
            case category if "Sun" in category:
                value  = f"{amount:4.0f}"
            case _:
                value = amount

        return value


