 pyWeatherApp.

The project was written in SQL, this has got complex to my simple mind.
So, rewriting the project in Pandas - it looks simpler.

    Scans a given directory for excel spreadsheets the contains daily weather data.
    A report can ne generated of the maximum and minimum values of all time.

To install dependencies pip -r requirements.txt

```
┌────────────────────────────────── pyWeatherApp 2025.6 ──────────────────────────────────┐
│ This program comes with ABSOLUTELY NO WARRANTY; for details type `pyWeatherApp -l'.     │
│ This is free software, and you are welcome to redistribute it under certain conditions. │
└──────────────────────────── Copyright (C) 2025  Kevin Scott ────────────────────────────┘

usage: main.py [-h] [-l] [-v] [-e] [-c] [-cD] [-b] [-A] [-Z]

Builds a main data store out of individual weather data spreadsheets.

options:
  -h, --help          show this help message and exit
  -l, --license       Print the Software License.
  -v, --version       Print the version of the application.
  -e, --explorer      Load program working directory into file explorer.
  -c, --check         Check database integrity.
  -cD, --checkDelete  Check database integrity and delete unwanted.
  -b, --build         Build the data - consolidate the spreadsheets.
  -A, --Areport       Report on the data - finds the all time highs and lows.
  -Z, --Zap           Delete [Zap] both data and file stores.

 Kevin Scott (C) 2025 :: pyWeatherApp V2025.7
```

For changes see history.txt
