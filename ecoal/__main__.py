from time import sleep
from io import StringIO
import sys
import os
from getpass import getpass
from ecoal import Login
from ecoal import get_day_url
from ecoal import get_day_path
from ecoal import get_last_day_file
from ecoal import get_last_day_file_timestamp
from ecoal import download_day
from ecoal import download_day_file
from ecoal import update_dir

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("\tpython ecoal <IP_ADDRESS> <USER>\n")
        print("\tWhen the program runs, enter the password.")
        return
    login = Login(sys.argv[-2], sys.argv[-1], getpass())

    dir_path = "data"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    update_dir(login, dir_path) # Download and save an every day since the last saved timestamp
    df = download_day(login) # Download the current day
    if df is not None:
        timestamp = df["timestamp"].iloc[-1] # Get the latest timestamp
    else:
        print("No data from today.", file=sys.stderr)
    while True:
        sleep(30) # Check every 30 sec

        df = download_day(login) # Download the current day
        if df is None:
            print("No data from today.", file=sys.stderr)
            continue
        df = df.loc[(df["timestamp"] > timestamp)] # Extract new data

        if len(df) > 0:
            try:
                # Print new data to stdout and save it to the .csv file
                df.to_csv(get_day_path(dir_path), mode='a', header=False, index=False)
                s = StringIO()
                df.to_csv(s, index=False, sep=",", header=False)
                print(s.getvalue(), end="")
                timestamp = df["timestamp"].iloc[-1] # Get the latest timestamp
            except PermissionError:
                print("Permission to %s denied." % get_day_path(dir_path), file=sys.stderr)
            except Exception as e:
                print(e, file=sys.stderr)
            
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("Exiting.", file=sys.stderr)