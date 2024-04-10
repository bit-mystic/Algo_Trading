from  datetime import datetime as dt
start = dt.now()

import pandas as pd 
import math

def rn(n, r=0.05):
    return n - math.fmod(n, r)

symbol = "SBIN"
his_data = pd.read_csv("store.csv",header=0,index_col=0)
total = len(his_data)
total_amount = 100000
risk_reward=3
sl_spread=2
riskpertrade=0.02

qty = 0
buy = 1
buy_date =2
sli = 3
tgt = 4
ext = 5
ext_date = 6
res = 7
per_gain=8
isAct = 9
trades = []
indices = []


def is_consolidating(ind,per,period):
    recent_candles = his_data[ind-period:ind]
    max_close = recent_candles["High"].max()
    min_close = recent_candles["Low"].min()
    inv = 1-per
    if min_close>inv*max_close:
        return True
    else:
        return False

def is_breaking(ind,per,period):
    if is_consolidating(ind-1,per,period):
        recent_candles = his_data[ind-period-1:ind-1]
        ma_clos = recent_candles["High"].max()
        if his_data["High"][ind] > ma_clos:
            return True
        else:
            return False
        
def trail_stop(ind):
    for trs in trades:
        if trs[isAct]==True:
            if his_data["Close"][ind]>(trs[sli]+1.5*sl_spread):
                trs[sli]=rn(trs[sli]+sl_spread)
                trs[sli]=rn(trs[sli]*0.99)


def consolidation_backtesting(period=15,per=0.25):
    global sl_spread
    global total_amount
    in_trade = False
    for ind in range(period+1,total-1):
        curr_close = his_data["Close"][ind]
        curr_open = his_data["Open"][ind]
        curr_high = his_data["High"][ind]
        curr_low = his_data["Low"][ind]
        for trs in trades:
            if trs[isAct]==True:
                if trs[sli] > curr_low:
                    if trs[sli] > curr_open:
                        trs[ext]=rn(curr_open*0.995)
                    else:
                        trs[ext]=trs[sli]
                    trs[isAct] = False
                    trs[res]=trs[ext]*trs[qty]*0.998-trs[buy]*trs[qty]*1.005-15
                    # total_amount=total_amount+trs[buy]*trs[qty]*1.005
                    total_amount=total_amount+trs[res]
                    trs[ext_date]=his_data["Date"][ind]
                    trs[per_gain]=(trs[res]*100)/(trs[buy]*trs[qty])
                    in_trade = False
                else:
                    if trs[tgt]<curr_high:
                        if trs[tgt] < curr_open:
                            trs[ext] = curr_open
                        else:
                            trs[ext] = trs[tgt]
                        trs[isAct] = False
                        trs[res]=trs[ext]*trs[qty]*0.9988-trs[buy]*trs[qty]*1.005-15
                        # total_amount=total_amount+trs[buy]*trs[qty]*1.005
                        total_amount=total_amount+trs[res]
                        trs[ext_date]=his_data["Date"][ind]
                        trs[per_gain]=(trs[res]*100)/(trs[buy]*trs[qty])
                        in_trade=False
        # trail_stop(ind)
        if in_trade:
            continue
        if is_breaking(ind,per,period):
            recent_candles = his_data[ind-period-1:ind-1]
            ma_clos = recent_candles["High"].max()
            buy_price = rn(ma_clos*1.001)
            sl = rn(recent_candles["Low"].min()*0.99999)
            if curr_open>ma_clos:
                buy_price=rn(curr_open*1.001)
                sl = rn(ma_clos*0.98)
            sl_spread=rn(buy_price-sl)
            target = rn(buy_price+risk_reward*(sl_spread))
            quantity = int((riskpertrade*total_amount)/(sl_spread))
            if quantity==0:
                continue;
            in_trade = True
            # total_amount=total_amount-buy_price*quantity*1.005
            trades.append([quantity,buy_price,his_data["Date"][ind],sl,target,00,his_data["Date"][ind],00,0,True])
            indices.append(ind)

consolidation_backtesting()

if len(trades)>0:
    trades = pd.DataFrame(trades)
    trades.columns = ["Quantity","Buy_Price","Date_Time(Entry)","Stop_Loss","Target","Exit_Price","Date_Time(Exit)","Result","(Gain/Loss)%","IsActive"]
# print("The results after backtesting this stradegy on {} is:".format(symbol))
# print(trades)
print(total_amount)

file_name = "Consolidation_"+symbol+'_Result.xlsx'
trades.to_excel(file_name)

print("The results after backtesting this stradegy on {} is successfully saved in the file specified.".format(symbol))

end = dt.now()

td = (end - start).total_seconds() * 10**3
print(f"The time of execution of above program is : {td:.03f}ms")

