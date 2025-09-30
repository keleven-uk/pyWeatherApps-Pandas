#################################################################################################################################
#    args   Copyright (C) <2025>  <Kevin Scott>                                                                                 #
#                                                                                                                               #
#    Parse the command line arguments.                                     .                                                    #
#                                                                                                                               #
# options:                                                                                                                      #
#   -h, --help          show this help message and exit                                                                         #
#   -l, --license       Print the Software License.                                                                             #
#   -v, --version       Print the version of the application.                                                                   #
#   -e, --explorer      Load program working directory into file explorer.                                                      #
#   -i, --info          Print info on the data store [Pandas dataFrame].                                                        #
#   -c, --check         Check data store integrity.                                                                             #
#   -cD, --checkDelete  Check data store integrity and delete unwanted.                                                         #
#   -b, --build         Build the data data store - consolidate the spreadsheets.                                               #
#   -D, --Dreport       Report on the data data store - finds the Daily highs and lows, for a given year, month and day.        #
#   -M, --Mreport       Report on the data data store - finds the monthly highs and lows, for a given month and year.           #
#   -T, --Treport       Report on the data data store - finds the monthly highs and lows, for a given month across all years.   #
#   -Y, --Yreport       Report on the data data store - finds the yearly highs and lows, for a given year.                      #
#   -A, --Areport       Report on the data data store - finds the all time highs and lows.                                      #
#   -P, --Plot PLOT     Plot a line graph of the table, -H for column selection.                                                #
#   -H, --PlotHelp      Display the column selection for plotting.                                                              #
#   -y, --year YEAR     Year of data files to report on.                                                                        #
#   -m, --month MONTH   Month of data files to report on.                                                                       #
#   -d, --day DAY       Day of data files to report on.                                                                         #
#   -Z, --Zap           Delete [Zap] both data and file stores.                                                                 #
#                                                                                                                               #
#     For changes see history.txt                                                                                               #
#                                                                                                                               #
#################################################################################################################################
#                                                                                                                               #
#    This program is free software: you can redistribute it and/or modify it under the terms of the                             #
#    GNU General Public License as published by the Free Software Foundation, either Version 3 of the                           #
#    License, or (at your option) any later Version.                                                                            #
#                                                                                                                               #
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without                          #
#    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                 #
#    GNU General Public License for more details.                                                                               #
#                                                                                                                               #
#    You should have received a copy of the GNU General Public License along with this program.                                 #
#    If not, see <http://www.gnu.org/licenses/>.                                                                                #
#                                                                                                                               #
################################################################################################################################

import sys
import textwrap
import argparse
import calendar

from datetime import datetime

import src.utils.dataUtils as utils
import src.classes.periodStore as ps
import src.utils.arguments as ag

############################################################################################## parseArgs ######
def parseArgs(Config, logger):
    """  Process the command line arguments.

         Checks the arguments and will exit if not valid.

         Exit code 0 - program has exited normally, after print version, licence or help.

         Exit Code 3 - exits with an error.

         The arguments for day, moth and year are validated here and only valid values are returned.
         If a non-valid values is entered, an error message is displayed and exit.

         Maybe the validation shouldn't be here - but kinda works.
    """
    pStore    = ps.PeriodStore(logger)          #  Create the period store, holds year and month that contain data.
    arguments = ag.Arguments()                  #  Create the class [dataclass], holds the command line arguments.

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""\
        Builds a main data store out of individual weather data spreadsheets.
        """),
        epilog=f" Kevin Scott (C) 2025 :: {Config.NAME} V{Config.VERSION}")

    parser.add_argument("-x",  "--license",     action="store_true", help="Print the Software License.")
    parser.add_argument("-v",  "--version",     action="store_true", help="Print the version of the application.")
    parser.add_argument("-e",  "--explorer",    action="store_true", help="Load program working directory into file explorer.")
    parser.add_argument("-i",  "--info",        action="store_true", help="Print info on the data store [Pandas dataFrame].")
    parser.add_argument("-c",  "--check",       action="store_true", help="Check data store integrity.")
    parser.add_argument("-cD", "--checkDelete", action="store_true", help="Check data store integrity and delete unwanted.")
    parser.add_argument("-b",  "--build",       action="store_true", help="Build the data data store - consolidate the spreadsheets.")
    parser.add_argument("-l",  "--location",    action="store",      help="Specify the location of the weather data -L for options.")
    parser.add_argument("-L",  "--locations",   action="store_true", help="Displays the available locations of weather data.")
    parser.add_argument("-D",  "--Dreport",     action="store_true", help="Report on the data data store - finds the Daily highs and lows, for a given year, month and day.")
    parser.add_argument("-M",  "--Mreport",     action="store_true", help="Report on the data data store - finds the monthly highs and lows, for a given month and year.")
    parser.add_argument("-T",  "--Treport",     action="store_true", help="Report on the data data store - finds the monthly highs and lows, for a given month across all years.")
    parser.add_argument("-Y",  "--Yreport",     action="store_true", help="Report on the data data store - finds the yearly highs and lows, for a given year.")
    parser.add_argument("-A",  "--Areport",     action="store_true", help="Report on the data data store - finds the all time highs and lows.")
    parser.add_argument("-P",  "--Plot",        type = int, required=False, default=0,
                                                action="store",      help="Plot a line graph of the table, -H for column selection.")
    parser.add_argument("-H",  "--PlotHelp",    action="store_true", help="Display the column selection for plotting.")
    parser.add_argument("-y",  "--year",        action="store",      help="Year of data files to report on.")
    parser.add_argument("-m",  "--month",       action="store",      help="Month of data files to report on.")
    parser.add_argument("-d",  "--day",         action="store",      help="Day of data files to report on.")
    parser.add_argument("-Z",  "--Zap",         action="store_true", help="Delete [Zap] both data and file stores.")

    args = parser.parse_args()

    arguments.plot     = args.Plot  if args.Plot  else 0
    arguments.plotHelp = True if args.PlotHelp else False
    arguments.version  = True if args.version  else False
    arguments.license  = True if args.license  else False
    arguments.explorer = True if args.explorer else False
    arguments.info     = True if args.info     else False
    arguments.build    = True if args.build    else False
    arguments.Areport  = True if args.Areport  else False
    arguments.Yreport  = True if args.Yreport  else False
    arguments.Mreport  = True if args.Mreport  else False
    arguments.Dreport  = True if args.Dreport  else False
    arguments.Treport  = True if args.Treport  else False
    arguments.Zap      = True if args.Zap      else False
    arguments.year     = args.year  if args.year  else 0
    arguments.month    = args.month if args.month else ""
    arguments.day      = args.day   if args.day   else 0
    arguments.location = args.location if args.location else "All"

    if args.locations:
        print("Available locations of weather data.")
        for loc in Config.LOCATIONS:
            print(f"{loc}", end=" ")
        print()
        print("Goodbye.")
        sys.exit(0)

    if args.location:
        if args.location in Config.LOCATIONS:
            location = args.location
        else:
            displayError(logger, f"ERROR :: {args.location} is not a valid location.  See -L for options")

    arguments.checkDB = 0
    if args.check:
        arguments.checkDB = 1                    # Run data integrity check in test mode on library.
    elif args.checkDelete:
        arguments.checkDB = 2                    # Run data integrity check in delete mode on library.

    if args.year:
        """  Checks that the given year has data associated with it.
             If there is no data for that year, display and error and exit.
        """
        if not pStore.hasYear(args.year):
            displayError(logger, f"ERROR :: {args.year} is not a valid year {pStore.listYears()}.")

    if args.month:
        """  Checks that the given month is a valid month name.
             If a non-valid month is given, display an error message and exit.
             If there is no data for that month, display an error message and exit.
        """
        month = args.month.capitalize()
        if month not in calendar.month_name[1:]:
            displayError(logger, f"ERROR :: {args.month} is not a valid month.")

    if args.day:
        """  Checks that the given day number actually exists for that month.
             If a non-valid day is given, display an error message and exit.

             The weather station was moved location on the 16-07-2025 - so no data.
        """
        day         = int(args.day)
        year        = int(args.year)
        intMonth    = list(calendar.month_name).index(args.month)
        daysInMonth = calendar.monthrange(year, intMonth)[1]

        if year == 2025 and intMonth == 7 and day == 16:
            displayError(logger, "No data for this day, weather station moveing between Gilberdyke and Hedon.")

        if not (0 <= day <= daysInMonth):
            displayError(logger, f"ERROR :: Not in day range for {args.year} {month} [0-{daysInMonth}].")
        if intMonth == datetime.now().month > datetime.now().day:
            displayError(logger, f"ERROR :: Future day : {day} is after today {datetime.now().day}.")

    if args.year and args.month:
        """  The weather data starts in July 2023, so display error and exit  if earlier month is given.
        """
        if args.year == "2023" and args.month in ["January", "February", "March", "April", "May", "June"]:
            displayError(logger, "ERROR :: Data for 2023 starts in July.", "danger")

    if args.Yreport:
        """  If year[-Y] is given, check there is a year value.
        """
        if not (args.year):
            displayError(logger, "ERROR :: With -Y [year] option a value of year[-y] must be given.")

    if args.Mreport:
        """  If month[-M] is given, check there is a year and month value.
        """
        if not (args.year and args.month):
            displayError(logger, "ERROR :: With -M [month] option a value of year[-y] and month[-m] must be given.")
        if args.Mreport and not pStore.hasMonth(args.year, args.month):
            displayError(logger, f"ERROR :: No data for {args.year} {month} yet.")

    if args.Treport:
        """  If month[-M] is given, check there is a year and month value.
        """
        if not (args.month):
            displayError(logger, "ERROR :: With -T [month] option a value of month[-m] must be given.")

    if args.Dreport:
        """  If moth[-D] is given, check there is a year, month and day value.
        """
        if not (args.year and args.month and args.day):
            displayError(logger, "ERROR :: With -D [day] option a value of year[-y] and month[-m] and day[-d] must be given.")

    return arguments

def displayError(logger, message):
    utils.logPrint(logger, True, message, "danger")
    utils.logPrint(logger, False, "-" * 100, "info")
    print("Goodbye.")
    sys.exit(3)

