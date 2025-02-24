###############################################################################################################
#    weatherUtils.py    Copyright (C) <2025>  <Kevin Scott>                                                   #
#                                                                                                             #
#    Utility functions for weather reporting.                                                                 #
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



def hourStreak(dfData):
    """  Iterated through the weather data and looks for the longest streak of wet or dry hours.

         The input is a Pandas data frame holding the weather data.
           It should contain at least two columns "Date" and "Rain Hourly"

         The output is a string containing the start and end dates of the streak and the length in hours.
    """
    dfData.columns = dfData.columns.str.replace(" ","_")        # No spaces in tuple headers.
    dfData["Rain_Hourly"] = dfData["Rain_Hourly"].fillna(0)     # Just in case any exist.

    raining     = False
    draught     = False
    daysDrought = 0
    daysRaining = 0
    strkDrought = 0
    strkRaining = 0
    tmpDrought  = ""
    tmpRaining  = ""
    strtRaining = dfData["Date"].iloc[0]
    endRaining  = dfData["Date"].iloc[0]
    strtDrought = dfData["Date"].iloc[0]
    endDrought  = dfData["Date"].iloc[0]

    for row in dfData.itertuples():
        date = row.Date
        rain = row.Rain_Hourly

        match rain:
            case 0:
                if raining:                                     #  Start of a drought.
                    if daysRaining > strkRaining:
                        strkRaining = daysRaining
                        strtRaining = tmpRaining
                        endRaining  = date
                    raining      = False
                    draught      = True
                    daysDrought += 1
                    daysRaining  = 0
                    tmpDrought   = date
                else:
                    draught      = True
                    daysDrought += 1
            case rain if rain > 0:
                if draught:                                     #  Start of a raining streak.
                    if daysDrought > strkDrought:
                        strkDrought = daysDrought
                        strtDrought = tmpDrought
                        endDrought  = date
                    raining      = True
                    draught      = False
                    daysDrought  = 0
                    daysRaining += 1
                    tmpRaining   = date
                else:
                    raining      = True
                    daysRaining += 1
            case _:                                             #  Ignore NaN values and reset streaks.
                print("should not happen")
                daysDrought = 0
                daysRaining = 0

    if daysRaining > strkRaining:                               #  In case all the dataframe is raining or draught.
        strkRaining = daysRaining
        endRaining  = date

    if daysDrought > strkDrought:
        strkDrought = daysDrought
        endDrought = date

    dtStartRaining = strtRaining.to_pydatetime()
    dtEndRaining   = endRaining.to_pydatetime()
    dtStartDrought = strtDrought.to_pydatetime()
    dtEndDrought   = endDrought.to_pydatetime()


    diffRaining = (dtEndRaining - dtStartRaining).total_seconds() / 3600
    diffDrought = (dtEndDrought - dtStartDrought).total_seconds() / 3600

    rain    = f" On {strtRaining.strftime("%d-%m-%Y, %H:%M")} it rained for  {diffRaining:0.2f} Hours"
    draught = f" On {strtDrought.strftime("%d-%m-%Y, %H:%M")} it was dry for {diffDrought:0.2f} Hours"

    # rain    = f" It rained between {strtRaining.strftime("%d-%m-%Y, %H:%M")} and {endRaining.strftime("%d-%m-%Y, %H:%M")} for {diffRaining:0.2f} Hours"
    # draught = f"It was dry between {strtDrought.strftime("%d-%m-%Y, %H:%M")} and {endDrought.strftime("%d-%m-%Y, %H:%M")} for {diffDrought:0.2f} Hours"

    return (rain, draught)


def dayStreak(dfData):
    """  Iterated through the weather data and looks for the longest streak of wet or dry days.

         The input is a Pandas data frame holding the weather data.
           It should contain at least two columns "Date" and "Rain Daily"

         The output is a string containing the start and end dates of the streak and the length in days.
    """
    dfData.columns = dfData.columns.str.replace(" ","_")    # No spaces in tuple headers.
    dfData["Rain_Daily"] = dfData["Rain_Daily"].fillna(0)   # Just in case any exist.

    raining     = False
    draught     = False
    daysDrought = 0
    daysRaining = 0
    strkDrought = 0
    strkRaining = 0
    tmpDrought  = ""
    tmpRaining  = ""
    strtRaining = dfData["Date"].iloc[0]
    endRaining  = dfData["Date"].iloc[0]
    strtDrought = dfData["Date"].iloc[0]
    endDrought  = dfData["Date"].iloc[0]
    newDate     = dfData["Date"].iloc[0]                    #  Initialise to the first row.
    newRain     = dfData["Rain_Daily"].iloc[0]              #  Initialise to the first row.

    for row in dfData.itertuples():
        oldDate = newDate                                   #  remember yesterdays data.
        oldRain = newRain
        newDate = row.Date
        newRain = row.Rain_Daily

        if newDate.day != oldDate.day:                      #  Only check rain data at the turn of the day.

            match oldRain:
                case 0:
                    if raining:                             #  Start of a drought.
                        if daysRaining > strkRaining:
                            strkRaining = daysRaining
                            strtRaining = tmpRaining
                            endRaining  = oldDate
                        raining      = False
                        draught      = True
                        daysDrought += 1
                        daysRaining  = 0
                        tmpDrought   = oldDate
                    else:
                        draught      = True
                        daysDrought += 1
                case oldRain if oldRain > 0:
                    if draught:                             #  Start of a raining streak.
                        if daysDrought > strkDrought:
                            strkDrought = daysDrought
                            strtDrought = tmpDrought
                            endDrought  = oldDate
                        raining      = True
                        draught      = False
                        daysDrought  = 0
                        daysRaining += 1
                        tmpRaining   = oldDate
                    else:
                        raining      = True
                        daysRaining += 1
                case _:                                     #  Ignore NaN values and reset streaks.
                    print("should not happen")
                    daysDrought = 0
                    daysRaining = 0

    if daysRaining > strkRaining:                           #  In case all the dataframe is raining or draught.
                    strkRaining = daysRaining
                    endRaining  = oldDate

    if daysDrought > strkDrought:
                    strkDrought = daysDrought
                    endDrought  = oldDate

    dtStartRaining = strtRaining.to_pydatetime()
    dtEndRaining   = endRaining.to_pydatetime()
    dtStartDrought = strtDrought.to_pydatetime()
    dtEndDrought   = endDrought.to_pydatetime()

    diffRaining = (dtEndRaining - dtStartRaining).total_seconds() / 86400
    diffDrought = (dtEndDrought - dtStartDrought).total_seconds() / 86400

    rain    = f" On {strtRaining.strftime("%d-%m-%Y, %H:%M")} it rained for  {diffRaining:0.2f} Days"
    draught = f" On {strtDrought.strftime("%d-%m-%Y, %H:%M")} it was dry for {diffDrought:0.2f} Days"
    # rain    = f" It rained between {strtRaining.strftime("%d-%m-%Y, %H:%M")} and {endRaining.strftime("%d-%m-%Y, %H:%M")} for {diffRaining:0.2f} Days"
    # draught = f"It was dry between {strtDrought.strftime("%d-%m-%Y, %H:%M")} and {endDrought.strftime("%d-%m-%Y, %H:%M")} for {diffDrought:0.2f} Days"

    return (rain, draught)
