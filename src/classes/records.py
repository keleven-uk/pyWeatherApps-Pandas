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

            match category:
                case "Outdoor Temperature" | "Outdoor Feels Like" | "Outdoor Dew Point" | "Outdoor Humidity" | "Indoor Temperature" | "Indoor Humidity":
                    maxDate    = data[0]
                    maxAmount  = self.formatValue(category, data[1])
                    minDate    = data[2]
                    minAmount  = self.formatValue(category, data[3])
                    meanAmount = self.formatValue(category, data[4])
                case "Solar" | "UVI" | "Wind Speed" | "Wind Gust":
                    maxDate    = data[0]
                    maxAmount  = self.formatValue(category, data[1])
                    minDate    = ""
                    minAmount  = ""
                    meanAmount = ""
                case "Wind Direction":
                    continue
                case "Rain Rate" | "Rain Daily" | "Rain Event" | "Rain Hourly" | "Rain Weekly" | "Rain Monthly" | "Rain Yearly" | "Rain Yearly":
                    maxDate    = data[0]
                    maxAmount  = self.formatValue(category, data[1])
                    minDate    = ""
                    minAmount  = ""
                    meanAmount = ""
                case "Pressure Relative" | "Pressure Absolute":
                    maxDate    = data[0]
                    maxAmount  = self.formatValue(category, data[1])
                    minDate    = data[2]
                    minAmount  = self.formatValue(category, data[3])
                    meanAmount = self.formatValue(category, data[4])
                case "Days":
                    category  = "Consecutive Days of Rain/Drought"
                    maxDate   = data[0]
                    maxAmount = f"{self.formatValue("Days", data[1])} Wet days"
                    minDate   = data[2]
                    minAmount = f"{self.formatValue("Days", data[3])} Dry days"
                case "Hour":
                    category  = "Consecutive Hours of Rain/Drought"
                    maxDate   = data[0]
                    maxAmount = f"{self.formatValue("Hour", data[1])} Wet hours"
                    minDate   = data[2]
                    minAmount = f"{self.formatValue("Hour", data[3])} Dry hours"
                case "Sun Consecutive":
                    category  = "Consecutive Days of Sun/No Sun"
                    maxDate   = data[0]
                    maxAmount = f"{self.formatValue("Sun Consecutive", data[1])} Sunny days"
                    minDate   = data[2]
                    minAmount = f"{self.formatValue("Sun Consecutive", data[3])} Dull days"
                case "Sun Total":
                    category  = "Total Days of Sun/No Sun"
                    maxDate    = ""
                    maxAmount = f"{self.formatValue("Sun Total", data[0])} Sunny days"
                    minDate    = ""
                    minAmount = f"{self.formatValue("Sun Total", data[1])} Dull days"

            #  Add horizontal lines after "Rain Yearly" is present, otherwise after "Rain Monthly"
            #  "Rain Yearly" is only present on all time and year reports.
            if "Rain Yearly" in reportValues:
                match category:
                    case "Outdoor Humidity" | "Indoor Humidity" | "UVI" | "Rain Yearly" | "Wind Gust" | "Pressure Absolute":
                        Table.add_row(f"{category}", f"{maxDate}", f"{maxAmount}", f"{minDate}", f"{minAmount}", f"{meanAmount}", end_section=True)
                    case _:
                        Table.add_row(f"{category}", f"{maxDate}", f"{maxAmount}", f"{minDate}", f"{minAmount}", f"{meanAmount}",)
            else:
                match category:
                    case "Outdoor Humidity" | "Indoor Humidity" | "UVI" | "Rain Monthly" | "Wind Gust" | "Pressure Absolute":
                        Table.add_row(f"{category}", f"{maxDate}", f"{maxAmount}", f"{minDate}", f"{minAmount}", f"{meanAmount}", end_section=True)
                    case _:
                        Table.add_row(f"{category}", f"{maxDate}", f"{maxAmount}", f"{minDate}", f"{minAmount}", f"{meanAmount}",)

        console.print(Table)

    #-------------------------------------------------------------------------------- formatDate(self, category, amount) ---------------------------
    def formatValue(self, category, amount):
        """  Format values correctly and add imperial equivalents, if appropriate.
        """
        match category:
            case category if "Temperature" in category:
                value  = f"{amount:3.2f}\N{DEGREE SIGN}C"
            case category if "Dew Point" in category:
                value  = f"{amount:3.2f}\N{DEGREE SIGN}C"
            case category if "Feels Like" in category:
                value  = f"{amount:3.2f}\N{DEGREE SIGN}C"
            case category if category.startswith("Rain"):
                value  = f"{amount:5.1f}mm ({amount*0.0393701:4.2f}in)"
            case category if category.startswith("Wind"):
                value  = f"{amount:3.2f} km/h ({amount*0.6213715277778:.2f}mph)"
            case category if category.startswith("Solar"):
                value  = f"{amount} Klux"
            case category if category.startswith("Pressure"):
                value  = f"{amount:4.0f} hPa"
            case category if "Humidity" in category:
                value  = f"{amount:3.2f}%"
            case category if "Days" in category:
                value  = f"{amount:4.0f}"
            case category if "Hour" in category:
                value  = f"{amount:4.0f}"
            case category if "Sun" in category:
                value  = f"{amount:4.0f}"
            case _:
                value = amount

        return value


