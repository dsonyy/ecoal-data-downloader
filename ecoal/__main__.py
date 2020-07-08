from ecoal import get_last_saved_timestamp
from ecoal import save_day
from ecoal import download_day
from ecoal import download_data

def main():
    print(get_last_saved_timestamp())
    download_data()

if __name__ == "__main__":
    main()