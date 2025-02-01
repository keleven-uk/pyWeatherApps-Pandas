 pyWeatherApp.

The project was written in SQL, this has got complex to my simple mind.
So, rewriting the project in Pandas - it looks simpler.

Scans a given directory for excel spreadsheets the contains daily weather data.
A report can then be generated of the maximum, minimum and mean values for of all time, monthly and yearly.

To install dependencies pip -r requirements.txt

```
┌─────────────────────────────────── pyWeather 2025.12 ───────────────────────────────────┐
│ This program comes with ABSOLUTELY NO WARRANTY; for details type `pyWeather -l'.        │
│ This is free software, and you are welcome to redistribute it under certain conditions. │
└──────────────────────────── Copyright (C) 2025  Kevin Scott ────────────────────────────┘

usage: main.py [-h] [-l] [-v] [-e] [-i] [-c] [-cD] [-b] [-M] [-Y] [-A] [-P PLOT] [-H] [-y YEAR] [-m MONTH] [-Z]

Builds a main data store out of individual weather data spreadsheets.

options:
  -h, --help            show this help message and exit
  -l, --license         Print the Software License.
  -v, --version         Print the version of the application.
  -e, --explorer        Load program working directory into file explorer.
  -i, --info            Print info on the data store [Pandas dataFrame].
  -c, --check           Check data store integrity.
  -cD, --checkDelete    Check data store integrity and delete unwanted.
  -b, --build           Build the data data store - consolidate the spreadsheets.
  -M, --Mreport         Report on the data data store - finds the monthly highs and lows.
  -Y, --Yreport         Report on the data data store - finds the yearly highs and lows.
  -A, --Areport         Report on the data data store - finds the all time highs and lows.
  -P PLOT, --Plot PLOT  Plot a line graph of the table, -H for column selection.
  -H, --PlotHelp        Display the column selection for plotting.
  -y YEAR, --year YEAR  Year of data files to report on.
  -m MONTH, --month MONTH
                        Month of data files to report on.
  -Z, --Zap             Delete [Zap] both data and file stores.

 Kevin Scott (C) 2025 :: pyWeather V2025.14
```

For changes see history.txt

```
┌────────────────────────────────── pyWeatherApp 2025.8 ──────────────────────────────────┐
│ This program comes with ABSOLUTELY NO WARRANTY; for details type `pyWeatherApp -l'.     │
│ This is free software, and you are welcome to redistribute it under certain conditions. │
└──────────────────────────── Copyright (C) 2025  Kevin Scott ────────────────────────────┘

                                   Weather Records for 2023 ** only from July **
─────────────────────┬───────────────────┬───────────────────────┬───────────────────┬───────────┬─────────────────┐
            Category │ Date              │ Max Value             │ Date              │ Min Value │ Mean Value      │
─────────────────────┼───────────────────┼───────────────────────┼───────────────────┼───────────┼─────────────────┤
 Outdoor Temperature │ 09-09-2023, 15:50 │ 31.40°C               │ 02-12-2023, 06:00 │ -4.00°C   │ 12.54°C         │
  Outdoor Feels Like │ 09-09-2023, 14:55 │ 31.40°C               │ 02-12-2023, 18:35 │ -4.70°C   │ 12.31°C         │
   Outdoor Dew Point │ 09-09-2023, 10:20 │ 20.50°C               │ 02-12-2023, 06:00 │ -4.10°C   │ 9.69°C          │
    Outdoor Humidity │ 09-07-2023, 01:30 │ 99.00°C               │ 07-07-2023, 15:20 │ 36.00°C   │ 84.27°C         │
  Indoor Temperature │ 05-11-2023, 13:05 │ 31.80°C               │ 16-12-2023, 07:25 │ 14.30°C   │ 22.06°C         │
     Indoor Humidity │ 03-08-2023, 06:00 │ 75.00°C               │ 03-09-2023, 14:15 │ 38.00°C   │ 57.55°C         │
               Solar │ 04-07-2023, 13:25 │ 132694.20°C           │                   │           │                 │
                 UVI │ 03-07-2023, 14:40 │ 10.0                  │                   │           │                 │
           Rain Rate │ 04-08-2023, 13:00 │   34mm (1.32in)       │                   │           │                 │
          Rain Daily │ 18-09-2023, 14:05 │   30mm (1.18in)       │                   │           │                 │
          Rain Event │ 21-10-2023, 14:55 │   45mm (1.77in)       │                   │           │                 │
         Rain Hourly │ 18-09-2023, 05:55 │   14mm (0.57in)       │                   │           │                 │
         Rain Weekly │ 05-08-2023        │   59mm (2.31in)       │                   │           │   11mm (0.42in) │
        Rain Monthly │ July 2023         │  120mm (4.71in)       │                   │           │   44mm (1.72in) │
          Wind Speed │ 21-12-2023, 08:50 │ 36.40 km/h (22.62mph) │                   │           │                 │
           Wind Gust │ 09-12-2023, 21:50 │ 62.30 km/h (38.71mph) │                   │           │                 │
   Pressure Relative │ 16-12-2023, 07:45 │ 1033 hPa              │ 02-11-2023, 10:00 │  959 hPa  │ 1006 hPa        │
   Pressure Absolute │ 16-12-2023, 07:45 │ 1036 hPa              │ 02-11-2023, 10:00 │  963 hPa  │ 1010 hPa        │
─────────────────────┴───────────────────┴───────────────────────┴───────────────────┴───────────┴─────────────────┘

16:43:08] pyWeather Completed :: 2.34s
          End of pyWeather 2025.13
```

![](resources\Tempratures_2023.jpg)
