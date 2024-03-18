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

stock=["NSE:SBIN-EQ"]
qty=51

buy_price = 754
below_leg = 750.9
above_leg = 755.1
sl_block=10
in_trade = False
side=-1
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
        if side==1:
            if message['ltp']>=buy_price:
                data = {
                    "symbol": stock[0],
                    "qty": qty,
                    "type": 2,
                    "side": side,
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
                    fyers.unsubscribe(symbols=stock,data_type="SymbolUpdate")
                    fyers.close_connection()
                else:
                    in_trade = True
                    sl_block=buy_price-below_leg
                    print("Position Taken in",stock[0])
        if side==-1:
            if message['ltp']<=buy_price:
                data = {
                    "symbol": stock[0],
                    "qty": qty,
                    "type": 2,
                    "side": side,
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
                    fyers.unsubscribe(symbols=stock,data_type="SymbolUpdate")
                    fyers.close_connection()
                else:
                    in_trade = True
                    sl_block=above_leg-buy_price
                    print("Position Taken in",stock[0])

    else:
        if (message['ltp'] <= below_leg or message['ltp'] >= above_leg):
            data = {}
            response = fyers1.exit_positions(data=data)
            if response["s"] == "ok":
                in_trade=False
                print("Positions Closed.")
                fyers.unsubscribe(symbols=stock,data_type="SymbolUpdate")
                fyers.close_connection()
            else:
                print("ALERT!! ACTION REQUIRED:",response["message"])
                fyers.unsubscribe(symbols=stock,data_type="SymbolUpdate")
                fyers.close_connection()
        elif side==-1:
            if (buy_price-message['ltp'])>sl_block:
                buy_price=buy_price-sl_block
                above_leg=above_leg-sl_block
                # below_leg=below_leg-sl_block
                print("Stop Loss Adjusted To",above_leg)
        elif side==1:
            if (message['ltp']-buy_price)>sl_block:
                buy_price=buy_price+sl_block
                # above_leg=above_leg+sl_block
                below_leg=below_leg+sl_block
                print("Stop Loss Adjusted To",below_leg)


def onerror(message):
    print("Error:", message)


def onclose(message):
    print("Connection closed:", message)


def onopen():
    fyers.subscribe(symbols=stock, data_type="SymbolUpdate")
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