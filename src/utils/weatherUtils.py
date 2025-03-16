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

#-------------------------------------------------------------------------------- rainAmount(dfData) ---------------------------
def rainAmount(dfData):
    """  Iterate through the weather data and sums the daily rain totals.

         The input is a Pandas data frame holding the weather data.
         It should contain at least two columns "Date" and "Daily Rain"

         The output a single integer..

         There is a bug in the Ecowitt softwere, the yearly rain fall is not reset at new year.
    """
    dfData.columns = dfData.columns.str.replace(" ","_")                      # No spaces in tuple headers.
    dfData["Rain_Daily"] = dfData["Rain_Daily"].fillna(0)                     # Just in case any exist.

    oldDate = ""
    rainSum = 0
    oldRain = 0

    for row in dfData.itertuples():
        date = row.Date.strftime("%d-%m-%Y")
        rain = row.Rain_Daily

        if date != oldDate:
            rainSum += oldRain
            oldDate  = date
        oldRain = rain


    rainSum += oldRain
    return rainSum
#-------------------------------------------------------------------------------- daysSunshine(dfData) ---------------------------
def daysSunshine(dfData):
    """  Iterate through the weather data and looks for the longest streak days with sunshine.
         Sunshine is defined by a Solar value of over 100000 Lux [1000 Klux].

         Footcandles is the Imperial measurement and Lux is the Metric measurement of the same thing.
         1 footcandle = 10.764 lux.
         Both quantify the amount of light falling on a specific point or object.

         The input is a Pandas data frame holding the weather data.
         It should contain at least two columns "Date" and "Solar"

         The output a tuple containing the start dates and length of sun/dull days.
    """
    dfData["Solar"] = dfData["Solar"].fillna(0)                     # Just in case any exist.

    solarLevel = 9290.304       #  Light intensity is returned if fc [footcandles]
    oldDate    = ""
    maxSolar   = 0
    daysSun    = 0
    daysDull   = 0
    strkSun    = 0
    strkDull   = 0
    totalSun   = 0
    totalDull  = 0
    tmpSun     = ""
    tmpDull    = ""
    dateSun    = ""

    for row in dfData.itertuples():
            date  = row.Date.strftime("%d-%m-%Y")
            solar = row.Solar

            if solar > maxSolar:
                maxSolar = solar

            if date != oldDate:
                oldDate = date

                if maxSolar > solarLevel:
                    totalSun += 1
                    daysSun  += 1
                    daysDull  = 0
                    if daysSun == 1:
                        tmpSun = date
                    if daysSun > strkSun:
                        strkSun = daysSun
                        dateSun = tmpSun
                else:
                    totalDull += 1
                    daysDull  += 1
                    daysSun    = 0
                    if daysDull == 1:
                        tmpDull = date
                    if daysDull > strkDull:
                        strkDull = daysDull
                        dateDull = tmpDull

                maxSolar  = 0

    return (dateSun, strkSun, dateDull, strkDull, totalSun, totalDull)
#-------------------------------------------------------------------------------- hoursRain(dfData) ---------------------------
def hoursRain(dfData):
    """  Iterate through the weather data and looks for the longest streak of wet or dry hours.

         The input is a Pandas data frame holding the weather data.
           It should contain at least two columns "Date" and "Rain Hourly"

         The output a tuple containing the start dates and length of rain/dry hours.
    """
    dfData.columns = dfData.columns.str.replace(" ","_")        # No spaces in tuple headers.
    dfData["Rain_Hourly"] = dfData["Rain_Hourly"].fillna(0)     # Just in case any exist.

    raining     = False
    draught     = False
    daysDrought = 0
    daysRaining = 0
    strkDrought = 0
    strkRaining = 0
    tmpDrought  = dfData["Date"].iloc[0]
    tmpRaining  = dfData["Date"].iloc[0]
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

    return (strtRaining.strftime("%d-%m-%Y, %H:%M"), diffRaining, strtDrought.strftime("%d-%m-%Y, %H:%M"), diffDrought)
#-------------------------------------------------------------------------------- daysRain(dfData) ---------------------------
def daysRain(dfData):
    """  Iterate through the weather data and looks for the longest streak of wet or dry days.

         The input is a Pandas data frame holding the weather data.
           It should contain at least two columns "Date" and "Rain Daily"

         The output a tuple containing the start dates and length of rain/dry days.
    """
    dfData.columns = dfData.columns.str.replace(" ","_")    # No spaces in tuple headers.
    dfData["Rain_Daily"] = dfData["Rain_Daily"].fillna(0)   # Just in case any exist.

    raining     = False
    draught     = False
    daysDrought = 0
    daysRaining = 0
    strkDrought = 0
    strkRaining = 0
    tmpDrought  = dfData["Date"].iloc[0]
    tmpRaining  = dfData["Date"].iloc[0]
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

    return (strtRaining.strftime("%d-%m-%Y"), diffRaining, strtDrought.strftime("%d-%m-%Y"), diffDrought)
