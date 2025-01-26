 pyWeatherApp.

The project was written in SQL, this has got complex to my simple mind.
So, rewriting the project in Pandas - it looks simpler.

Scans a given directory for excel spreadsheets the contains daily weather data.
A report can then be generated of the maximum and minimum values for of all time, monthly and yearly.

To install dependencies pip -r requirements.txt

```
┌────────────────────────────────── pyWeatherApp 2025.9 ──────────────────────────────────┐
│ This program comes with ABSOLUTELY NO WARRANTY; for details type `pyWeatherApp -l'.     │
│ This is free software, and you are welcome to redistribute it under certain conditions. │
└──────────────────────────── Copyright (C) 2025  Kevin Scott ────────────────────────────┘

usage: main.py [-h] [-l] [-v] [-e] [-c] [-cD] [-b] [-M] [-Y] [-A] [-y YEAR] [-m MONTH] [-Z]

Builds a main data store out of individual weather data spreadsheets.

options:
  -h, --help            show this help message and exit
  -l, --license         Print the Software License.
  -v, --version         Print the version of the application.
  -e, --explorer        Load program working directory into file explorer.
  -c, --check           Check database integrity.
  -cD, --checkDelete    Check database integrity and delete unwanted.
  -b, --build           Build the data - consolidate the spreadsheets.
  -M, --Mreport         Report on the data - finds the monthly highs and lows.
  -Y, --Yreport         Report on the data - finds the yearly highs and lows.
  -A, --Areport         Report on the data - finds the all time highs and lows.
  -y YEAR, --year YEAR  Year of data files.
  -m MONTH, --month MONTH
                        Month of data files.
  -Z, --Zap             Delete [Zap] both data and file stores.

 Kevin Scott (C) 2025 :: pyWeatherApp V2025.9

D:\My\shed\Projects\python\pyWeather - Pandas (main -> origin)                                                       
```

For changes see history.txt

```
┌────────────────────────────────── pyWeatherApp 2025.8 ──────────────────────────────────┐
│ This program comes with ABSOLUTELY NO WARRANTY; for details type `pyWeatherApp -l'.     │
│ This is free software, and you are welcome to redistribute it under certain conditions. │
└──────────────────────────── Copyright (C) 2025  Kevin Scott ────────────────────────────┘

[22:07:02] Start of pyWeatherApp 2025.8                                                                                                                                                                                                                                                                   dataUtils.py:51

                       Weather Records for 2023

┌─────────────────────────┬───────────────────┬──────────────────────┐
│                Category │ Date              │ Value                │
├─────────────────────────┼───────────────────┼──────────────────────┤
│ Outdoor Temperature_max │ 09-09-2023, 15:50 │ 31.40°C              │
│ Outdoor Temperature_min │ 02-12-2023, 06:00 │ -4.00°C              │
│  Outdoor Feels Like_max │ 09-09-2023, 14:55 │ 31.4°C               │
│  Outdoor Feels Like_min │ 02-12-2023, 18:35 │ -4.7°C               │
│   Outdoor Dew Point_max │ 09-09-2023, 10:20 │ 20.5°C               │
│   Outdoor Dew Point_min │ 02-12-2023, 06:00 │ -4.1°C               │
│    Outdoor Humidity_max │ 09-07-2023, 01:30 │ 99.0%                │
│    Outdoor Humidity_min │ 07-07-2023, 15:20 │ 36.0%                │
├─────────────────────────┼───────────────────┼──────────────────────┤
│  Indoor Temperature_max │ 05-11-2023, 13:05 │ 31.80°C              │
│  Indoor Temperature_min │ 16-12-2023, 07:25 │ 14.30°C              │
│     Indoor Humidity_max │ 03-08-2023, 06:00 │ 75%                  │
│     Indoor Humidity_min │ 03-09-2023, 14:15 │ 38%                  │
├─────────────────────────┼───────────────────┼──────────────────────┤
│               Solar_max │ 04-07-2023, 13:25 │ 132694.2 Klux        │
│                 UVI_max │ 03-07-2023, 14:40 │ 10.0                 │
├─────────────────────────┼───────────────────┼──────────────────────┤
│           Rain Rate_max │ 04-08-2023, 13:00 │   34mm (1.32in)      │
│          Rain Daily_max │ 18-09-2023, 14:05 │   30mm (1.18in)      │
│          Rain Event_max │ 21-10-2023, 14:55 │   45mm (1.77in)      │
│         Rain Hourly_max │ 18-09-2023, 05:55 │   14mm (0.57in)      │
│         Rain Weekly_max │ 05-08-2023        │   59mm (2.31in)      │
│        Rain Monthly_max │ July 2023         │  120mm (4.71in)      │
├─────────────────────────┼───────────────────┼──────────────────────┤
│          Wind Speed_max │ 21-12-2023, 08:50 │ 36.4 km/h (22.62mph) │
│           Wind Gust_max │ 09-12-2023, 21:50 │ 62.3 km/h (38.71mph) │
├─────────────────────────┼───────────────────┼──────────────────────┤
│   Pressure Relative_max │ 16-12-2023, 07:45 │ 1033 hPa             │
│   Pressure Relative_min │ 02-11-2023, 10:00 │  959 hPa             │
│   Pressure Absolute_max │ 16-12-2023, 07:45 │ 1036 hPa             │
│   Pressure Absolute_min │ 02-11-2023, 10:00 │  963 hPa             │
└─────────────────────────┴───────────────────┴──────────────────────┘

[22:07:04] pyWeatherApp Completed :: 1.61s                                                                                                                                                                                                                                                                dataUtils.py:51
           End of pyWeatherApp 2025.8
```
