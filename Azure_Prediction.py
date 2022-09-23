import urllib.request
import json
import os
import ssl
import pandas as pd

"""
Instructions:
URL retrieved from:
https://portal.azure.com/#home - Machine Learning - Project - Studio Web URL - Endpoints - Model - Consume
Send dataframe to endpoint, endpoint sends to model, model returns result.
Only need to maintain model_helper. The functions called in main derive from helper
"""


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


url = 'http://url.azurecontainer.io/' # azure endpoint url


def model_helper_Azure(X_test: pd.DataFrame, url: str):
    X_dict = X_test.to_dict('records')

    # encode = str -> bytes, decode = bytes -> str. this line tries to format in json a dict
    body = str.encode(json.dumps({"data": X_dict}))

    # URL from the Endpoint
    api_key = '' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = urllib.request.Request(url, body, headers) # Request(url, data, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        r = float(result.decode('UTF-8')[15:-3])
        print("Azure Model Prediction:", r)
        return r

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
        return None


def Azure_predict_model(X_test):
    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
    return model_helper_Azure(X_test, url)
