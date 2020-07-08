import requests
from requests.auth import HTTPBasicAuth
from io import StringIO
import time
import pandas as pd

IP = "192.168.1.29"
PASSWORD = "root"
USER = "root"

def get_day_url(day=None, month=None, year=None, ip=IP):
    if year == None: year = time.localtime().tm_year
    if month == None: month = time.localtime().tm_mon
    if day == None: day = time.localtime().tm_mday
    return "http://" + str(ip) + "/arch/" + str(year) + "/" + str(month).zfill(2) + "/ARCH" + str(day).zfill(2) + ".CSV"

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
    
    "t2_value":	        "",

    "kot_tact":	        "Temperatura zadana",
    "ob1_pok_tact":	    "Temperatura wewn. CO1",
    "ob1_pok_tzad":     "Temperatura zadana wewn. CO1",
    "ob1_zaw4d_tzad":	"Temperatura zadana za zaworem CO1",
    "ob1_zaw4d_pos":    "",
    "ob2_pok_tact":	    "",
    "ob2_pok_tzad":     "",
    "cwu_tact":	        "Temperatura zadana CWU",
    "ob3_pok_tact":	    "",
    "ob3_pok_tzad":	    "",
    "ob3_zaw4d_tzad":   "",
    "ob3_zaw4d_pos":	"",
    "ob3_t1":	        "",
    "ob3_t2":	        "",
    "ob4_pok_tact":	    "",
    "ob4_pok_tzad":     "",
    "ob4_zaw4d_tzad":	"",
    "ob4_zaw4d_pos":	"",
    "ob4_t1":	        "",
    "ob4_t2":           "",
    "ob5_pok_tact":     "",
    "ob5_pok_tzad":	    "",
    "ob5_zaw4d_tzad":	"",
    "ob5_zaw4d_pos":	"",
    "ob5_t1":	        "",
    "ob5_t2":           "",
    "ob6_pok_tact":     "",
    "ob6_pok_tzad":     "",
    "ob6_zaw4d_tzad":   "",
    "ob6_zaw4d_pos":    "",
    "ob6_t1":	        "",
    "ob6_t2":           "",
    }

    day_data = day_data.decode()
    day_data = StringIO(day_data)
    day_data = pd.read_csv(day_data, ";")
    # day_data.datetime = pd.to_datetime(day_data.datetime + TIMEZONE_OFFSET, unit="s") # convert dates
    day_data = day_data.iloc[:, :-1] # remove last unnamed column
    day_data.rename(columns={
        }, inplace=True)
        
    return day_data

def download_day_data(day=None, month=None, year=None, user=USER, password=PASSWORD, ip=IP):
    response = requests.get(
        get_day_url(day, month, year, ip), 
        auth=HTTPBasicAuth(user, password), 
        timeout=1)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return process_day_data(response.content)