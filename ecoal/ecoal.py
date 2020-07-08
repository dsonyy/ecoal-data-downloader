import requests
from requests.auth import HTTPBasicAuth
from io import StringIO
import time
import pandas as pd
import os
from datetime import datetime, timedelta

IP = "192.168.1.29"
PASSWORD = "root"
USER = "root"
DIR = os.path.normpath("./data/")

def get_day_url(day=None, month=None, year=None, ip=IP):
    if year == None: year = datetime.now().year
    if month == None: month = datetime.now().month
    if day == None: day = datetime.now().day
    return "http://%s/arch/%s/%02d/ARCH%02d.CSV" % (ip, year, month, day)

def get_day_path(day=None, month=None, year=None, dir=DIR):
    if year == None: year = datetime.now().year
    if month == None: month = datetime.now().month
    if day == None: day = datetime.now().day
    return os.path.join(dir, "%d-%02d-%02d.csv" % (year, month, day))


def process_day_data(day_data):
    NAMES = {
    "tkot_value":	    "Temperatura kotła",
    "tpow_value":	    "Temperatura powrotu",
    "tpod_value":	    "Temperatura podajnika",    
    "tcwu_value":       "Temperatura CWU",
    "twew_value":	    "Temperatura wewn. CO1",
    "tzew_value":	    "Temperatura zewnętrzna",
    "t1_value":	        "Temperatura za zawrotem",
    "tsp_value":        "Temperatura spalin",
    "tzew_act":         "Temperatura zewnętrzna",
    }

    day_data = day_data.decode()
    day_data = StringIO(day_data)
    day_data = pd.read_csv(day_data, ";")
    day_data = day_data.iloc[:, :-1] # remove last unnamed column
    day_data.rename(columns=NAMES, inplace=True)
        
    return day_data

def get_last_saved_day(dir=DIR):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    files.sort()
    if not files:
        return None
    latest = pd.read_csv(os.path.join(dir, files[-1]), sep=",")
    return latest

def get_last_saved_timestamp(dir=DIR):
    last_day = get_last_saved_day(dir)
    if last_day is None:
        return None
    return last_day.iloc[-1, 0]

def save_day(day_data, dir=None, last_timestamp=None):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    files.sort()
    latest = pd.read_csv(os.path.join(dir, files[-1]), sep=";")
    timestamp = latest.iloc[-1, 0]
    # day_data.loc[(day_data.datetime >= timestamp)]    

def download_day(day=None, month=None, year=None, user=USER, password=PASSWORD, ip=IP, dir=None):
    response = requests.get(
        get_day_url(day, month, year, ip), 
        auth=HTTPBasicAuth(user, password), 
        timeout=1)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    day_data = process_day_data(response.content)
    if dir:
        if year == None: year = datetime.now().year
        if month == None: month = datetime.now().month
        if day == None: day = datetime.now().day
        try:
            day_data.to_csv(get_day_path(day, month, year), sep=",", index=False)
        except Exception as e:
            print(e)
    return day_data
        
def download_data(since_timestamp=None, user=USER, password=PASSWORD, dir=DIR, ip=IP):
    if since_timestamp == None: since_timestamp = get_last_saved_timestamp(dir)
    day = datetime.fromtimestamp(since_timestamp)
    today = datetime.now() + timedelta(days=1)
    while day <= today:
        download_day(day.day, day.month, day.year, user=user, password=password, dir=dir, ip=ip)
        day += timedelta(days=1)
