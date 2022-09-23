from TWS import get_data_TWS
from SlackMsg import msg
from Azure_Prediction import Azure_predict_model
from GCP_Prediction import GCP_predict_model
from features import features_Azure, features_GCP

import datetime
import time

Slack_url = "https://hooks.slack.com/services/some_address_code"
while True:
    if datetime.datetime.now().second % 5 == 0: # Customize frequency of process
        # get raw data
        raw_data = get_data_TWS()
        time.sleep(0.1)
        print(raw_data)

        # process data
        data_Azure = features_Azure(raw_data)
        data_GCP = features_GCP(raw_data)

        # prediction
        prediction_Azure = Azure_predict_model(data_Azure)
        prediction_GCP = GCP_predict_model(data_GCP)

        # Slack
        msg("Current time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), Slack_url)
        for item in raw_data:
            msg(item + ": " + str(raw_data[item]), Slack_url)
        msg("Azure Prediction: " + str(prediction_Azure), Slack_url)
        msg("GCP Prediction: " + str(prediction_GCP), Slack_url)
