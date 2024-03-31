from datetime import datetime,date,timedelta
# import time
# from fyers_apiv3 import fyersModel

# f = open('acesstoken.txt', 'r')
# access_token = f.readline()
# f.close()
# client_id="L7YNNXJALM-100"
# fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

# spot = ["NSE:FINNIFTY-INDEX"]
since = date.today()-timedelta(days=-7)
to = date.today()
present=datetime.now()
print(since)
print(type(to))
present.hour
# while present.hour<8:
#     time.sleep(3600)
#     present=datetime.now()
# while present.hour<9:
#     time.sleep(900)
#     present=datetime.now()
# while present.minute<14:
#     time.sleep(60)
#     present=datetime.now()
# while present.minute<15:
#     time.sleep(0.5)
#     present=datetime.now()
# while present.hour<15:
#     if present.minute % 5 == 0:
#         data = {
#             "symbol":spot[0],
#             "resolution":"5",
#             "date_format":"1",
#             "range_from":str(since),
#             "range_to":str(to),
#             "cont_flag":"1"
#         }
#         response = fyers.history(data=data)