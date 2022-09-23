""" Slack API app """

import requests
import yfinance as yf
import numpy as np
import time

"""
Instructions:
- Workspace drop-down - Administration - Manage apps - Build - Create New App - From Scratch - Create App
- Incoming Webhooks Activate - Add New Webhook to Workspace - Select Channel
- Copy Webhook url and use in main.py
"""

def msg(message, url): 
    sent = "{'text':'%s'}" % message #json formatted message sent to Slack api
    response = requests.post(url, data=sent) #send the message to the api to post to channel
    print(response.text + ": " + message) #confirm on console that it was sent


"""
# simulation for testing
if __name__ == "__main__":
    dat = yf.download("AAPL")
    aapl = dat["Adj Close"][-1]
    url = "https://hooks.slack.com/services/some_address_code"
    # simulate GBM
    z = np.random.normal(size=10)
    z[0] = 0
    z = np.cumsum(z)
    aapl_sim = aapl + z
    for i in range(len(aapl_sim)):
        msg("AAPL at time " + str(i) + ": " + str(aapl_sim[i]), url)
        time.sleep(0.5)
"""    
    