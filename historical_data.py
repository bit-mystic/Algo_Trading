from datetime import datetime as dt
start = dt.now()

f = open('acesstoken.txt', 'r')
access_token = f.readline()
f.close()

from fyers_apiv3 import fyersModel
import os
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

client_id="L7YNNXJALM-100"

fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path=os.getcwd())

symbol = "NSE:SBIN-EQ"
candle_size = "D"
since = date.today() - relativedelta(years=20)
to = date.today()
s_since = since

till = since + relativedelta(years=1,days=-1)
if till>to:
    till = to
data = {
    "symbol":symbol,
    "resolution":candle_size,
    "date_format":"1",
    "range_from":str(since),
    "range_to":str(till),
    "cont_flag":"1"
}
response = fyers.history(data=data)
his_data = pd.DataFrame(response["candles"])

since = till

while since<to:
    till = since + relativedelta(years=1,days=-1)
    if till>to:
        till = to
    data = {
        "symbol":symbol,
        "resolution":candle_size,
        "date_format":"1",
        "range_from":str(since),
        "range_to":str(till),
        "cont_flag":"1"
    }
    response = fyers.history(data=data)
    s_data = pd.DataFrame(response["candles"])
    his_data=pd.concat([his_data,s_data]).reset_index(drop=True)
    since = till 

his_data.columns = ["Date","Open","High","Low","Close","Volume"]
his_data["Date"]=pd.to_datetime(his_data["Date"],unit='s')

his_data.to_csv("store.csv")

print("Data Successfully Fetched from {} to {} for {}.".format(s_since,to,symbol))

end = dt.now()
td = (end - start).total_seconds() * 10**3
print(f"The time of execution of above program is : {td:.03f}ms")
