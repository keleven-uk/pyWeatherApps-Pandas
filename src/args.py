#############################################################################################################################
#    args   Copyright (C) <2025>  <Kevin Scott>                                                                             #
#                                                                                                                           #
#    Parse the command line arguments.                                     .                                                #
#                                                                                                                           #
#   positional arguments:                                                                                                   #
#     infile                                                                                                                #
#                                                                                                                           #
#   options:                                                                                                                #
#     -h, --help            show this help message and exit                                                                 #
#     -l, --license         Print the Software License.                                                                     #
#     -v, --version         Print the version of the application.                                                           #
#     -e, --explorer        Load program working directory into file explorer.                                              #
#                                                                                                                           #
#     For changes see history.txt                                                                                           #
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

import sys
import textwrap
import argparse
import calendar

import src.license as License
import src.projectPaths as pp
import src.utils.dataUtils as utils
import src.classes.periodStore as ps

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

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""\
        Builds a main data store out of individual weather data spreadsheets.
        """),
        epilog=f" Kevin Scott (C) 2025 :: {Config.NAME} V{Config.VERSION}")

    parser.add_argument("-l",  "--license",     action="store_true", help="Print the Software License.")
    parser.add_argument("-v",  "--version",     action="store_true", help="Print the version of the application.")
    parser.add_argument("-e",  "--explorer",    action="store_true", help="Load program working directory into file explorer.")
    parser.add_argument("-i",  "--info",        action="store_true",  help="Print info on the data store [Pandas dataFrame].")
    parser.add_argument("-c",  "--check",       action="store_true", help="Check data store integrity.")
    parser.add_argument("-cD", "--checkDelete", action="store_true", help="Check data store integrity and delete unwanted.")
    parser.add_argument("-b",  "--build",       action="store_true", help="Build the data data store - consolidate the spreadsheets.")
    parser.add_argument("-D",  "--Dreport",     action="store_true", help="Report on the data data store - finds the Daily highs and lows.")
    parser.add_argument("-M",  "--Mreport",     action="store_true", help="Report on the data data store - finds the monthly highs and lows.")
    parser.add_argument("-Y",  "--Yreport",     action="store_true", help="Report on the data data store - finds the yearly highs and lows.")
    parser.add_argument("-A",  "--Areport",     action="store_true", help="Report on the data data store - finds the all time highs and lows.")
    parser.add_argument("-P",  "--Plot", type = int, required=False, default=0,
                                                action="store",      help="Plot a line graph of the table, -H for column selection.")
    parser.add_argument("-H",  "--PlotHelp",    action="store_true", help="Display the column selection for plotting.")
    parser.add_argument("-y",  "--year",        action="store",      help="Year of data files to report on.")
    parser.add_argument("-m",  "--month",       action="store",      help="Month of data files to report on.")
    parser.add_argument("-d",  "--day",         action="store",      help="Day of data files to report on.")
    parser.add_argument("-Z",  "--Zap",         action="store_true", help="Delete [Zap] both data and file stores.")

    args = parser.parse_args()

    if args.PlotHelp:
        """  Display the index numbers of the available column headers - for plotting.
        """
        for index, column in enumerate(pp.columnHeaders[1:]):
            print(f"  {index+1} .. {column}")

    if args.version:
        print("")
        utils.logPrint(logger, True, f"Running on {sys.version} Python", "info")
        utils.logPrint(logger, True, f"End of {Config.NAME} V{Config.VERSION}: Printed version", "info")
        utils.logPrint(logger, False, "-" * 100, "info")
        print("Goodbye.")
        sys.exit(0)

    if args.license:
        License.printLongLicense(Config.NAME, Config.VERSION, logger)
        logger.info(f"End of {Config.NAME} V{Config.VERSION} : Printed Licence")
        utils.logPrint(logger, False, "-" * 100, "info")
        print("Goodbye.")
        sys.exit(0)

    if args.explorer:
        utils.loadExplorer(logger)              # Load program working directory n file explorer.
        print("Goodbye.")
        sys.exit(0)

    checkDB = 0
    if args.check:
        checkDB = 1                    # Run data integrity check in test mode on library.
    elif args.checkDelete:
        checkDB = 2                    # Run data integrity check in delete mode on library.

    if args.year:
        """  Checks that the given year has data associated with it.
             If there is no data for that year, display and error and exit.
        """
        if not pStore.hasYear(args.year):
            utils.logPrint(logger, True, f"ERROR :: {args.year} is not a valid year {pStore.listYears()}.", "danger")
            utils.logPrint(logger, False, "-" * 100, "info")
            print("Goodbye.")
            sys.exit(3)
    else:
        day = 0

    if args.month:
        """  Checks that the given month is a valid month name.
             If a non-valid month is given, display an error message and exit.
             If there is no data for that month, display an error message and exit.
        """
        month = args.month.capitalize()
        if month not in calendar.month_name[1:]:
            utils.logPrint(logger, True, f"ERROR :: {args.month} is not a valid month.", "danger")
            utils.logPrint(logger, False, "-" * 100, "info")
            print("Goodbye.")
            sys.exit(3)
        if not pStore.hasMonth(args.year, args.month):
            utils.logPrint(logger, True, f"ERROR :: No data for {args.year} {month} yet.", "danger")
            utils.logPrint(logger, False, "-" * 100, "info")
            print("Goodbye.")
            sys.exit(3)
    else:
        month = 0

    if args.day:
        """  Checks that the given day number actually exists for that month.
             If a non-valid day is given, display an error message and exit.
        """
        day         = int(args.day)
        daysInMonth = calendar.monthrange(2023, 1)[1]
        if not (0 <= day <= daysInMonth):
            utils.logPrint(logger, True, f"ERROR :: Not in day range for {args.year} {month} [0-{daysInMonth}].", "danger")
            utils.logPrint(logger, False, "-" * 100, "info")
            print("Goodbye.")
            sys.exit(3)
    else:
        day = 0

    if args.year and args.month:
        """  The weather data starts in July 2023, so display error and exit  if earlier month is given.
        """
        if args.year == "2023" and args.month in ["January", "February", "March", "April", "May", "June"]:
            utils.logPrint(logger, True, "ERROR :: Data for 2023 starts in July.", "danger")
            utils.logPrint(logger, False, "-" * 100, "info")
            print("Goodbye.")
            sys.exit(3)

    if args.Yreport:
        """  If year[-Y] is given, check there is a year value.
        """
        if not (args.year and args.month):
            utils.logPrint(logger, True, "ERROR :: With -Y [year] option a value of year[-y] must be given.", "danger")
            utils.logPrint(logger, False, "-" * 100, "info")
            print("Goodbye.")
            sys.exit(3)

    if args.Mreport:
        """  If month[-M] is given, check there is a year and month value.
        """
        if not (args.year and args.month):
            utils.logPrint(logger, True, "ERROR :: With -M [month] option a value of year[-y] and month[-m] must be given.", "danger")
            utils.logPrint(logger, False, "-" * 100, "info")
            print("Goodbye.")
            sys.exit(3)

    if args.Dreport:
        """  If moth[-D] is given, check there is a year, month and day value.
        """
        if not (args.year and args.month and args.day):
            utils.logPrint(logger, True, "ERROR :: With -D [day] option a value of year[-y] and month[-m]  and day[-d] must be given.", "danger")
            utils.logPrint(logger, False, "-" * 100, "info")
            print("Goodbye.")
            sys.exit(3)


    return args.build, args.Plot, args.info, checkDB, args.Areport, args.Yreport, args.Mreport, args.Dreport, args.year, month, day, args.Zap





