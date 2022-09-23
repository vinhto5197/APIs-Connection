from ibapi.client import EClient  # outgoing requests
from ibapi.wrapper import EWrapper  # incoming messages
from ibapi.contract import Contract

import threading
import time
import datetime
import pandas as pd

"""
Instructions:
-Log in to TWS live account (if paper, change to 7497 on app.connect())
-Edit – Global Configuration – API – Settings
-Tick Enable ActiveX and Socket Clients
-Untick Read-only API when implementing order executions
https://algotrading101.com/learn/interactive-brokers-python-api-native-guide/
"""

"""
tickType:
Bid: 1
Ask: 2
Last: 4
High: 6
Low: 7
Close: 9
Open: 14



# for full list of TickType
from ibapi.ticktype import TickTypeEnum

for i in range(91):
	print(TickTypeEnum.to_str(i), i)
"""

"""
Need to recheck reqID for desired stocks
Dummy reqID: 
AMZN: 1 
AAPL_High: 5 (part of AAPL)
AAPL_Low: 5 (part of AAPL)
AAPL: 5
"""


def get_data_TWS():
    raw_data = {"AAPL": None, "AAPL High": None, "AAPL Low": None, "AMZN": None}

    # Requesting data
    class IBapi(EWrapper, EClient):
        def __init__(self):
            EClient.__init__(self, self)

        def tickPrice(self, reqId, tickType, price):
            d = {1: "AMZN", 5: "AAPL"}
            if 9.5 <= datetime.datetime.now().hour + datetime.datetime.now().minute/60 <= 16: # market hour
                if tickType == 4: # last Price
                    raw_data[d[reqId]] = [price]
            else:
                if tickType == 9: # closing price. api won't feed last price during non-market hour
                    raw_data[d[reqId]] = [price]
            if reqId == 5 and tickType == 6: # AAPL high
                raw_data["AAPL High"] = [price]
            if reqId == 5 and tickType == 7: # AAPL low
                raw_data["AAPL Low"] = [price]

    def run_loop():
        app.run()

    app = IBapi()
    app.connect('127.0.0.1', 7496, 123)

    # Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()  # try to establish a connection as soon as this is called.

    # Sleep interval to allow time for connection to server. ERROR -1 (connected) starts from api_thread.start()
    time.sleep(1)

    # Create contract object
    aapl_contract = Contract()
    aapl_contract.symbol = "AAPL"
    aapl_contract.secType = "STK"
    aapl_contract.exchange = "SMART"
    aapl_contract.currency = "USD"

    amzn_contract = Contract()
    amzn_contract.symbol = "AMZN"
    amzn_contract.secType = "STK"
    amzn_contract.exchange = "SMART"
    amzn_contract.currency = "USD"

    # Request Market Data. Threading keeps calling tickprice until disconnect
    # tickPrice is called everytime there is an update in price.
    app.reqMktData(1, amzn_contract, '', False, False, [])
    app.reqMktData(5, aapl_contract, '', False, False, [])

    while True:
        # keep feeding data until everything is received.
        # data may be unavailable outside RTH. To test outside RTH, put out of loop.
        if None not in raw_data.values():
            break
    app.disconnect()

    df = pd.DataFrame.from_dict(raw_data)
    df["Date"] = datetime.datetime.today().strftime("%m/%d/%Y")
    first_col = df.pop("Date")
    df.insert(0, "Date", first_col)

    return df

