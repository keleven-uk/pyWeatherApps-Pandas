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
┌─────────────────────────────────── pyWeather 2025.17 ───────────────────────────────────┐                             
│ This program comes with ABSOLUTELY NO WARRANTY; for details type `pyWeather -l'.        │                             
│ This is free software, and you are welcome to redistribute it under certain conditions. │                             
└──────────────────────────── Copyright (C) 2025  Kevin Scott ────────────────────────────┘                             
                                                                                                                        
[16:47:35] Start of pyWeather 2025.17                                                                                   
                                               All Time Weather Records                                                 
┌─────────────────────┬───────────────────┬───────────────────────┬───────────────────┬───────────┬─────────────────┐   
│            Category │ Date              │ Max Value             │ Date              │ Min Value │ Mean Value      │   
├─────────────────────┼───────────────────┼───────────────────────┼───────────────────┼───────────┼─────────────────┤   
│ Outdoor Temperature │ 09-09-2023, 15:50 │ 31.40°C               │ 21-11-2024, 07:55 │ -6.90°C   │ 10.80°C         │   
│  Outdoor Feels Like │ 09-09-2023, 14:55 │ 31.40°C               │ 21-11-2024, 07:55 │ -6.90°C   │ 10.44°C         │   
│   Outdoor Dew Point │ 09-09-2023, 10:20 │ 20.50°C               │ 21-11-2024, 07:45 │ -8.00°C   │ 7.66°C          │   
│    Outdoor Humidity │ 09-07-2023, 01:30 │ 99.00%                │ 07-07-2023, 15:20 │ 36.00%    │ 82.17%          │   
├─────────────────────┼───────────────────┼───────────────────────┼───────────────────┼───────────┼─────────────────┤   
│  Indoor Temperature │ 05-11-2023, 13:05 │ 31.80°C               │ 17-04-2024, 07:00 │ 13.80°C   │ 21.53°C         │   
│     Indoor Humidity │ 03-08-2023, 06:00 │ 75.00%                │ 20-08-2024, 14:20 │ 32.00%    │ 55.49%          │   
├─────────────────────┼───────────────────┼───────────────────────┼───────────────────┼───────────┼─────────────────┤   
│               Solar │ 29-05-2024, 12:45 │ 139952.8 Klux         │                   │           │                 │   
│                 UVI │ 03-07-2023, 14:40 │ 10.0                  │                   │           │                 │   
├─────────────────────┼───────────────────┼───────────────────────┼───────────────────┼───────────┼─────────────────┤   
│           Rain Rate │ 04-08-2023, 13:00 │   34mm (1.32in)       │                   │           │                 │   
│          Rain Daily │ 18-09-2023, 14:05 │   30mm (1.18in)       │                   │           │                 │   
│          Rain Event │ 21-10-2023, 14:55 │   45mm (1.77in)       │                   │           │                 │   
│         Rain Hourly │ 18-09-2023, 05:55 │   14mm (0.57in)       │                   │           │                 │   
│         Rain Weekly │ 05-08-2023        │   59mm (2.31in)       │                   │           │    9mm (0.34in) │   
│        Rain Monthly │ July 2023         │  120mm (4.71in)       │                   │           │   35mm (1.39in) │   
├─────────────────────┼───────────────────┼───────────────────────┼───────────────────┼───────────┼─────────────────┤   
│          Wind Speed │ 21-12-2023, 08:50 │ 36.40 km/h (22.62mph) │                   │           │                 │   
│           Wind Gust │ 09-12-2023, 21:50 │ 62.30 km/h (38.71mph) │                   │           │                 │   
├─────────────────────┼───────────────────┼───────────────────────┼───────────────────┼───────────┼─────────────────┤   
│   Pressure Relative │ 11-01-2024, 16:45 │ 1038 hPa              │ 06-01-2025, 05:40 │  959 hPa  │ 1007 hPa        │   
│   Pressure Absolute │ 06-02-2025, 09:00 │ 1048 hPa              │ 02-11-2023, 10:00 │  963 hPa  │ 1013 hPa        │   
└─────────────────────┴───────────────────┴───────────────────────┴───────────────────┴───────────┴─────────────────┘   
Dry / Raining streaks by Hour                                                                                           
 On 28-04-2024, 02:40 it rained for  10.33 Hours                                                                        
 On 18-06-2024, 17:00 it was dry for 254.25 Hours                                                                       
Dry / Raining streaks by Day                                                                                            
 On 23-10-2023, 23:55 it rained for  17.00 Days                                                                         
 On 19-06-2024, 23:55 it was dry for 10.00 Days                                                                         
Table generated 24-02-2025  16:47                                                                                       
                                                                                                                        
[16:47:37] pyWeather Completed :: 2.59s                                                                                 
           End of pyWeather 2025.17                                                                                     
```

![](resources\Tempratures_2023.jpg)
