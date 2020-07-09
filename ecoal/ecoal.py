import requests
from requests.auth import HTTPBasicAuth
from io import StringIO
import time
import pandas as pd
import os
from datetime import datetime, timedelta
import sys

IP = "192.168.1.29"
PASSWORD = "root"
USER = "root"
DIR = os.path.normpath("./data/")

def get_day_url(day=None, month=None, year=None, ip=IP):
    if year == None: year = datetime.utcnow().year
    if month == None: month = datetime.utcnow().month
    if day == None: day = datetime.utcnow().day
    return "http://%s/arch/%s/%02d/ARCH%02d.CSV" % (ip, year, month, day)

def get_day_path(day=None, month=None, year=None, dir=DIR):
    if year == None: year = datetime.utcnow().year
    if month == None: month = datetime.utcnow().month
    if day == None: day = datetime.utcnow().day
    return os.path.join(dir, "%d-%02d-%02d.csv" % (year, month, day))

def get_last_day_file(dir=DIR):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    files.sort()
    if not files:
        return None
    latest = pd.read_csv(os.path.join(dir, files[-1]), sep=",")
    return latest

def get_last_day_file_timestamp(dir=DIR):
    last_day = get_last_day_file(dir)
    if last_day is None:
        return None
    return last_day.iloc[-1, 0]  

def process_day_raw(day_raw):
    NAMES = {
        "datetime":     "timestamp",
        "tkot_value":	"Temperatura kotła",
        "tpow_value":	"Temperatura powrotu",
        "tpod_value":	"Temperatura podajnika",    
        "tcwu_value":   "Temperatura CWU",
        "twew_value":	"Temperatura wewn. CO1",
        "tzew_value":	"Temperatura zewnętrzna",
        "t1_value":	    "Temperatura za zawrotem",
        "tsp_value":    "Temperatura spalin",
        "tzew_act":     "Temperatura zewnętrzna",
    }
    day_raw = day_raw.decode()
    day_raw = StringIO(day_raw)
    day_raw = pd.read_csv(day_raw, ";")
    day_raw = day_raw.iloc[:, :-1] # remove last unnamed column
    day_raw.rename(columns=NAMES, inplace=True)
    return day_raw

def download_day(day=None, month=None, year=None, user=USER, password=PASSWORD, ip=IP, dir=DIR):
    url = get_day_url(day, month, year, ip)
    response = requests.get(
        url, 
        auth=HTTPBasicAuth(user, password), 
        timeout=1)
    if response.status_code == 404:
        print("404 Server response error: ", url, file=sys.stderr)
        return None
    response.raise_for_status()
    return process_day_raw(response.content)

def download_day_file(day=None, month=None, year=None, user=USER, password=PASSWORD, ip=IP, dir=DIR):
    day_data = download_day(day, month, year, user, password, ip, dir)
    try:
        day_data.to_csv(get_day_path(day, month, year), sep=",", index=False)
        return day_data
    except Exception as e:
        print("Unable to save data to file: ", e, file=sys.stderr)
        
def update_dir(user=USER, password=PASSWORD, ip=IP, dir=DIR):
    since_timestamp = get_last_day_file_timestamp(dir)
    if since_timestamp is None:
        download_day_file(user=user, password=password, ip=ip, dir=dir)
        return
    day = datetime.utcnow()
    day_data = download_day_file(day.day, day.month, day.year, user, password, ip, dir)
    timestamp = day_data.iloc[0, 0]
    while timestamp >= since_timestamp:
        day -= timedelta(days=1)
        day_data = download_day_file(day.day, day.month, day.year, user, password, ip, dir)
        if day_data is None:
            continue
        timestamp = day_data.iloc[0, 0]
