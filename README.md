# eSterownik data downloader
A small piece of software which allows you to automatically download data from boilers equipped with **eSterownik** manufacturer's controller. It's an unofficial tool written for home purposes. The data is downloaded via local network, which eCoal controller is connected to.

Tested only on **eCoal-B V3.5**.

👷‍♂️ Work in progress...

## Features
- Download daily boiler statistics as a `pandas.DataFrame` or save them as a `.csv` file.
- Real-time download and update `.csv` file data.

## Examples
```py
import ecoal
login = ecoal.Login("192.168.1.XX", "user", "password")

# Download daily data as a pandas.DataFrame
df0 = ecoal.download_day(login)
df1 = ecoal.download_day(login, 25, 6, 2020)

# Download daily data and save it as a .csv file
ecoal.download_day_file(login, "data_dir")
ecoal.download_day_file(login, "data_dir", 25, 6, 2020)

# Get the last saved record from the data directory and download all later records
ecoal.update(login, dir="data_dir")
```
You can also run it as a standalone script:
```
python ecoal IP_ADDRESS USER
```

Then, you will be asked for the password. This script updates the data directory every 30 seconds.

**Additional notes:**
- There is a separate `.csv` file for each day (UTC+0). 
- Not every column of `.csv` files has a self-describing header because I'm not sure about them (e.g. *t2_value*, *ob4_t1*, *ob4_t2*).
