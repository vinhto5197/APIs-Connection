import pandas as pd
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

"""
Instructions:
conda prompt: 
pip install --upgrade google-cloud

"""


def model_helper(
    project: str,
    endpoint_id: str,
    X_test: pd.DataFrame,
    location: str = "region",
    api_endpoint: str = "region-aiplatform.googleapis.com",
):

    X_dict = X_test.to_dict("records")

    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # for more info on the instance schema, please use get_model_sample.py
    # and look at the yaml found in instance_schema_uri
    instance = json_format.ParseDict(X_dict, Value())
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )

    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    predictions = response.predictions
    
    for prediction in predictions:
        print("Prediction: ", dict(prediction)['classes'][0])
        print("Score:", dict(prediction)['scores'][0])

    return dict(prediction[0])['classes'][0]


def GCP_predict_model(project, endpoint_id, X_test, location, api_endpoint):
    return model_helper(project, endpoint_id, X_test, location, api_endpoint)