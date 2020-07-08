import requests
from requests.auth import HTTPBasicAuth
from io import StringIO
import time
import pandas as pd
import os

IP = "192.168.1.29"
PASSWORD = "root"
USER = "root"
DIR = os.path.normpath("./data/")

def get_day_url(day=None, month=None, year=None, ip=IP):
    if year == None: year = time.localtime().tm_year
    if month == None: month = time.localtime().tm_mon
    if day == None: day = time.localtime().tm_mday
    return "http://%s/arch/%s/%02d/ARCH%02d.CSV" % (ip, year, month, day)

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

def save_day_data(day_data, dir=None, last_timestamp=None):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    files.sort()
    latest = pd.read_csv(os.path.join(dir, files[-1]), sep=";")
    timestamp = latest.iloc[-1, 0]
    # day_data.loc[(day_data.datetime >= timestamp)]
    

def download_day_data(day=None, month=None, year=None, user=USER, password=PASSWORD, ip=IP, dir=None):
    response = requests.get(
        get_day_url(day, month, year, ip), 
        auth=HTTPBasicAuth(user, password), 
        timeout=1)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    day_data = process_day_data(response.content)
    if dir:
        if year == None: year = time.localtime().tm_year
        if month == None: month = time.localtime().tm_mon
        if day == None: day = time.localtime().tm_mday
        try:
            day_data.to_csv(dir + str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + ".csv", 
                sep=";", index=False)
        except Exception as e:
            print(e)
        
    
