 pyWeatherApp.

The project was written in SQL, this has got complex to my simple mind.
So, rewriting the project in Pandas - it looks simpler.

Scans a given directory for excel spreadsheets the contains daily weather data.
A report can then be generated of the maximum, minimum and mean values for of all time, daily, monthly and yearly.

To install dependencies pip -r requirements.txt

```
┌─────────────────────────────────── pyWeather 2025.22 ───────────────────────────────────┐
│ This program comes with ABSOLUTELY NO WARRANTY; for details type `pyWeather -l'.        │
│ This is free software, and you are welcome to redistribute it under certain conditions. │
└──────────────────────────── Copyright (C) 2025  Kevin Scott ────────────────────────────┘

usage: main.py [-h] [-l] [-v] [-e] [-i] [-c] [-cD] [-b] [-D] [-M] [-T] [-Y] [-A] [-P PLOT] [-H] [-y YEAR] [-m MONTH] [-d DAY] [-Z]

Builds a main data store out of individual weather data spreadsheets.

options:
  -h, --help          show this help message and exit
  -l, --license       Print the Software License.
  -v, --version       Print the version of the application.
  -e, --explorer      Load program working directory into file explorer.
  -i, --info          Print info on the data store [Pandas dataFrame].
  -c, --check         Check data store integrity.
  -cD, --checkDelete  Check data store integrity and delete unwanted.
  -b, --build         Build the data data store - consolidate the spreadsheets.
  -D, --Dreport       Report on the data data store - finds the Daily highs and lows, for a given year, month and day..
  -M, --Mreport       Report on the data data store - finds the monthly highs and lows, for a given month and year.
  -T, --Treport       Report on the data data store - finds the monthly highs and lows, for a given month across all years.
  -Y, --Yreport       Report on the data data store - finds the yearly highs and lows, for a given year.
  -A, --Areport       Report on the data data store - finds the all time highs and lows.
  -P, --Plot PLOT     Plot a line graph of the table, -H for column selection.
  -H, --PlotHelp      Display the column selection for plotting.
  -y, --year YEAR     Year of data files to report on.
  -m, --month MONTH   Month of data files to report on.
  -d, --day DAY       Day of data files to report on.
  -Z, --Zap           Delete [Zap] both data and file stores.

 Kevin Scott (C) 2025 :: pyWeather V2025.22
```

For changes see history.txt

```
                                                        All Time Weather Records
┌───────────────────────────────────┬───────────────────┬───────────────────────┬───────────────────┬────────────────┬─────────────────┐
│                          Category │ Date              │ Max Value             │ Date              │ Min Value      │ Mean Value      │
├───────────────────────────────────┼───────────────────┼───────────────────────┼───────────────────┼────────────────┼─────────────────┤
│               Outdoor Temperature │ 09-09-2023, 15:50 │ 31.40°C               │ 21-11-2024, 07:55 │ -6.90°C        │ 10.77°C         │
│                Outdoor Feels Like │ 09-09-2023, 14:55 │ 31.40°C               │ 21-11-2024, 07:55 │ -6.90°C        │ 10.40°C         │
│                 Outdoor Dew Point │ 09-09-2023, 10:20 │ 20.50°C               │ 21-11-2024, 07:45 │ -8.00°C        │ 7.62°C          │
│                  Outdoor Humidity │ 09-07-2023, 01:30 │ 99.00%                │ 17-07-2023, 07:45 │ 0.00%          │ 81.99%          │
├───────────────────────────────────┼───────────────────┼───────────────────────┼───────────────────┼────────────────┼─────────────────┤
│                Indoor Temperature │ 05-11-2023, 13:05 │ 31.80°C               │ 17-04-2024, 07:00 │ 13.80°C        │ 21.53°C         │
│                   Indoor Humidity │ 03-08-2023, 06:00 │ 75.00%                │ 20-08-2024, 14:20 │ 32.00%         │ 55.46%          │
├───────────────────────────────────┼───────────────────┼───────────────────────┼───────────────────┼────────────────┼─────────────────┤
│                             Solar │ 29-05-2024, 12:45 │ 139952.8 Klux         │                   │                │                 │
│                               UVI │ 03-07-2023, 14:40 │ 10.0                  │                   │                │                 │
├───────────────────────────────────┼───────────────────┼───────────────────────┼───────────────────┼────────────────┼─────────────────┤
│                         Rain Rate │ 04-08-2023, 13:00 │   34mm (1.32in)       │                   │                │                 │
│                        Rain Daily │ 18-09-2023, 14:05 │   30mm (1.18in)       │                   │                │                 │
│                        Rain Event │ 21-10-2023, 14:55 │   45mm (1.77in)       │                   │                │                 │
│                       Rain Hourly │ 18-09-2023, 05:55 │   14mm (0.57in)       │                   │                │                 │
│                       Rain Weekly │ 05-08-2023        │   59mm (2.31in)       │                   │                │    8mm (0.32in) │
│                      Rain Monthly │ July 2023         │  120mm (4.71in)       │                   │                │   35mm (1.37in) │
├───────────────────────────────────┼───────────────────┼───────────────────────┼───────────────────┼────────────────┼─────────────────┤
│                        Wind Speed │ 21-12-2023, 08:50 │ 36.40 km/h (22.62mph) │                   │                │                 │
│                         Wind Gust │ 21-02-2025, 15:25 │ 64.40 km/h (40.02mph) │                   │                │                 │
├───────────────────────────────────┼───────────────────┼───────────────────────┼───────────────────┼────────────────┼─────────────────┤
│                 Pressure Relative │ 11-01-2024, 16:45 │ 1038 hPa              │ 06-01-2025, 05:40 │  959 hPa       │ 1007 hPa        │
│                 Pressure Absolute │ 06-02-2025, 09:00 │ 1048 hPa              │ 02-11-2023, 10:00 │  963 hPa       │ 1013 hPa        │
├───────────────────────────────────┼───────────────────┼───────────────────────┼───────────────────┼────────────────┼─────────────────┤
│ Consecutive Hours of Rain/Drought │ 28-04-2024, 02:40 │   10 Wet hours        │ 18-06-2024, 17:00 │  254 Dry hours │                 │
│  Consecutive Days of Rain/Drought │ 23-10-2023        │   17 Wet days         │ 19-06-2024        │   10 Dry days  │                 │
│    Consecutive Days of Sun/No Sun │ 15-06-2024        │   25 Sunny days       │ 30-08-2023        │  212 Dull days │                 │
└───────────────────────────────────┴───────────────────┴───────────────────────┴───────────────────┴────────────────┴─────────────────┘
Table generated 27-02-2025  21:38
```

![](resources/Tempratures_2023.jpg)
