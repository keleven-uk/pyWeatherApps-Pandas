#############################################################################################################################
#    args   Copyright (C) <202025>  <Kevin Scott>                                                                           #
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
import src.utils.dataUtils as utils

############################################################################################## parseArgs ######
def parseArgs(Config, logger):
    """  Process the command line arguments.

         Checks the arguments and will exit if not valid.

         Exit code 0 - program has exited normally, after print version, licence or help.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""\
        Builds a main data store out of individual weather data spreadsheets.
        """),
        epilog=f" Kevin Scott (C) 2025 :: {Config.NAME} V{Config.VERSION}")

    parser.add_argument("-l",  "--license",     action="store_true", help="Print the Software License.")
    parser.add_argument("-v",  "--version",     action="store_true", help="Print the version of the application.")
    parser.add_argument("-e",  "--explorer",    action="store_true", help="Load program working directory into file explorer.")
    parser.add_argument("-c",  "--check",       action="store_true", help="Check database integrity.")
    parser.add_argument("-cD", "--checkDelete", action="store_true", help="Check database integrity and delete unwanted.")
    parser.add_argument("-b",  "--build",       action="store_true", help="Build the data - consolidate the spreadsheets.")
    parser.add_argument("-M",  "--Mreport",     action="store_true", help="Report on the data - finds the monthly highs and lows.")
    parser.add_argument("-Y",  "--Yreport",     action="store_true", help="Report on the data - finds the yearly highs and lows.")
    parser.add_argument("-A",  "--Areport",     action="store_true", help="Report on the data - finds the all time highs and lows.")
    parser.add_argument("-y",  "--year",        action="store",      help="Year of data files.")
    parser.add_argument("-m",  "--month",       action="store",      help="Month of data files.")
    parser.add_argument("-Z",  "--Zap",         action="store_true", help="Delete [Zap] both data and file stores.")

    args = parser.parse_args()

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
        if args.year not in Config.REPORT_YEARS:
            utils.logPrint(logger, True, f"ERROR :: {args.year} is not a valid year {Config.REPORT_YEARS}.", "danger")
            utils.logPrint(logger, False, "-" * 100, "info")
            print("Goodbye.")
            sys.exit(3)
    else:                           #  If not year supplied, return config year.
        args.year = Config.YEAR

    if args.month:
        month = args.month.capitalize()
        if month not in calendar.month_name[1:]:
            utils.logPrint(logger, True, f"ERROR :: {args.month} is not a valid month.", "danger")
            utils.logPrint(logger, False, "-" * 100, "info")
            print("Goodbye.")
            sys.exit(3)
    else:                           #  If not month supplied, return config year.
        month = Config.MONTH

    #  The weather data starts in July 2023, so ignore if earlier month is given.
    #  Not user if should be here or else where - but stops me looking for errors that ain't there.'
    if args.year and args.month:
        if args.year == "2023" and args.month in ["January", "February", "March", "April", "May", "June"]:
            utils.logPrint(logger, True, "ERROR :: Data for 2023 starts in July.", "danger")
            utils.logPrint(logger, False, "-" * 100, "info")
            print("Goodbye.")
            sys.exit(3)


    return args.build, checkDB, args.Areport, args.Yreport, args.Mreport, args.year, month, args.Zap





