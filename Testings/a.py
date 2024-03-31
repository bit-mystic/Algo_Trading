from fyers_apiv3.FyersWebsocket import data_ws
from fyers_apiv3 import fyersModel
import math


def rn(n, r=50):
    return n - math.fmod(n, r)

f = open('acesstoken.txt', 'r')
access_token = f.readline()
f.close()
client_id = "L7YNNXJALM-100"
fyers1 = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")

spot = ["NSE:FINNIFTY-INDEX"]
lot_size = 40
contract = "NSE:FINNIFTY24FEB"
curr_price=0


def choosestrike(side, spot_price):
    global curr_price
    spr = rn(spot_price)
    if side == "PE":
        spr = spr+50
        data = {
            "symbols": contract+str(int(spr))+side
        }
        response = fyers1.quotes(data=data)
        while response["d"][0]["v"]["lp"] > 50:
            spr = spr-50
            data = {
                "symbols": contract+str(int(spr))+side
            }
            response = fyers1.quotes(data=data)
        curr_price=response["d"][0]["v"]["lp"]
        return spr
    else:
        data = {
            "symbols": contract+str(int(spr))+side
        }
        response = fyers1.quotes(data=data)
        while response["d"][0]["v"]["lp"] > 50:
            spr = spr+50
            data = {
                "symbols": contract+str(int(spr))+side
            }
            response = fyers1.quotes(data=data)
        curr_price=response["d"][0]["v"]["lp"]
        return spr


buy_price = 20640
below_leg = 20631
above_leg = 20670
sl_block=10
in_trade = False
short=False
initials=0

def onmessage(message):
    global initials
    if initials<3:
        initials=initials+1
        return
    global in_trade
    global sl_block
    global above_leg
    global below_leg
    global buy_price
    if in_trade == False:
        if short==False:
            if message['ltp'] >= buy_price:
                side = "CE"
                strike_price = choosestrike(side, message['ltp'])
                data = {
                    "symbol": contract+str(int(strike_price))+side,
                    "qty": lot_size,
                    "type": 2,
                    "side": 1,
                    "productType": "INTRADAY",
                    "limitPrice": 0,
                    "stopPrice": 0,
                    "validity": "DAY",
                    "disclosedQty": 0,
                    "offlineOrder": False,
                    "orderTag": "tag1"
                }
                response = fyers1.place_order(data=data)
                if response["s"] == "error":
                    print("Error while placing order:",response["message"])
                    fyers.unsubscribe(symbols=spot,data_type="SymbolUpdate")
                    fyers.close_connection()
                elif (response["s"] == "ok"):
                    in_trade = True
                    sl_block=buy_price-below_leg
        else:
            if message['ltp'] <= buy_price:
                side = "PE"
                strike_price = choosestrike(side, message['ltp'])
                data = {
                    "symbol": contract+str(int(strike_price))+side,
                    "qty": lot_size,
                    "type": 2,
                    "side": 1,
                    "productType": "INTRADAY",
                    "limitPrice": 0,
                    "stopPrice": 0,
                    "validity": "DAY",
                    "disclosedQty": 0,
                    "offlineOrder": False,
                    "orderTag": "tag1"
                }
                response = fyers1.place_order(data=data)
                if response["s"] == "error":
                    print("Error while placing order:",response["message"])
                    fyers.unsubscribe(symbols=spot,data_type="SymbolUpdate")
                    fyers.close_connection()
                elif (response["s"] == "ok"):
                    in_trade = True
                    sl_block=above_leg-buy_price
    else:
        if (message['ltp'] <= below_leg or message['ltp'] >= above_leg):
            data = {}
            response = fyers1.exit_positions(data=data)
            if response["s"] == "ok":
                in_trade=False
            else:
                print("ALERT!! ACTION REQUIRED:",response["message"])
                fyers.unsubscribe(symbols=spot,data_type="SymbolUpdate")
                fyers.close_connection()
        elif short==True:
            if (buy_price-message['ltp'])>sl_block:
                buy_price=buy_price-sl_block
                above_leg=above_leg-sl_block
                # below_leg=below_leg-sl_block
        elif short==False:
            if (message['ltp']-buy_price)>sl_block:
                buy_price=buy_price+sl_block
                # above_leg=above_leg+sl_block
                below_leg=below_leg+sl_block



def onerror(message):
    print("Error:", message)


def onclose(message):
    print("Connection closed:", message)


def onopen():
    fyers.subscribe(symbols=spot, data_type="SymbolUpdate")
    fyers.keep_running()


fyers = data_ws.FyersDataSocket(
    access_token=client_id+":"+access_token,
    log_path="",
    litemode=True,
    write_to_file=False,
    reconnect=True,
    on_connect=onopen,
    on_close=onclose,
    on_error=onerror,
    on_message=onmessage
)
fyers.connect()