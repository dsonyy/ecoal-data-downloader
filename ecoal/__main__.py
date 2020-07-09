from ecoal import get_day_url
from ecoal import get_day_path
from ecoal import get_last_day_file
from ecoal import get_last_day_file_timestamp
from ecoal import download_day
from ecoal import download_day_file
from ecoal import update_dir
from time import sleep
from io import StringIO
from sys import stderr

def main():
    update_dir()
    df = download_day()
    if df is not None:
        timestamp = df["timestamp"].iloc[-1]
    else:
        print("No data from today.", file=stderr)
        return
    while True:
        sleep(30)
        df = download_day()
        df = df.loc[(df["timestamp"] > timestamp)]
        if len(df) > 0:
            s = StringIO()
            df.to_csv(s, index=False, sep=",", header=False)
            print(s.getvalue(), end="")
            df.to_csv(get_day_path(), mode='a', header=False, index=False)

if __name__ == "__main__":
    main()