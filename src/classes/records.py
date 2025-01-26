###############################################################################################################
#    Records.py    Copyright (C) <2025>  <Kevin Scott>                                                        #
#                                                                                                             #
#    A class to hold records, this then subclassed to monthly, yearly and all time.                           #
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

    def show(self, title, reportValues):
        """  Prints to screen the contains of the records in a pretty table.

             reportValues - should hold a directory containing the data to display.
                            The key should be the column header and data the value, date.

             The title of the table needs to be passed in.
        """
        Table.title = title

        Table.add_column("Category", justify="right", style="cyan", no_wrap=True)
        Table.add_column("Date", style="magenta")
        Table.add_column("Value", justify="left", style="green")

        for key in reportValues:
            #   Ignore values we don't want to see.'
            if key in ["Solar_min", "UVI_min", "Rain Rate_min", "Rain Daily_min", "Rain Event_min", "Rain Hourly_min", "Rain Weekly_min",
                       "Rain Monthly_min", "Rain Yearly_min", "Wind Speed_min", "Wind Gust_min", "Wind Direction_max", "Wind Direction_min"]:
                continue

            data     = reportValues[key]
            category = key
            date     = data[0]
            amount   = data[1]

            #  Format values correctly and add imperial equivalents, if appropriate.
            match category:
                case category if "Temperature" in category:
                    value  = f"{amount:.2f}\N{DEGREE SIGN}C"
                case category if "Dew Point" in category:
                    value  = f"{amount}\N{DEGREE SIGN}C"
                case category if "Feels Like" in category:
                    value  = f"{amount}\N{DEGREE SIGN}C"
                case category if category.startswith("Rain"):
                    value  = f"{amount:4.0f}mm ({amount*0.0393701:4.2f}in)"
                case category if category.startswith("Wind"):
                    value  = f"{amount} km/h ({amount*0.6213715277778:.2f}mph)"
                case category if category.startswith("Solar"):
                    value  = f"{amount} Klux"
                case category if category.startswith("Pressure"):
                    value  = f"{amount:4.0f} hPa"
                case category if "Humidity" in category:
                    value  = f"{amount}%"
                case _:
                    value = amount

            #  Add horizontal lines to the table to split the categories
            match category:
                case "DayTimeTemperature_min" | "Outdoor Humidity_min" | "Indoor Humidity_min"| "UVI_max" |\
                     "Rain Monthly_max" | "Wind Gust_max":
                    Table.add_row(f"{category}", f"{date}", f"{value}", end_section=True)
                case _:
                    Table.add_row(f"{category}", f"{date}", f"{value}")

        console.print(Table)




