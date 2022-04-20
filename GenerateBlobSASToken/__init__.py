import logging
import azure.functions as func
import json
from azure.storage.blob import generate_blob_sas
from datetime import datetime, timedelta
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = json.dumps(req.get_json())
    except ValueError:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )
    
    if body:
        result = compose_response(body)
        return func.HttpResponse(result, mimetype="application/json")
    else:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )


def compose_response(json_data):
    values = json.loads(json_data)['values']
    
    # Prepare the Output before the loop
    results = {}
    results["values"] = []
    
    for value in values:
        output_record = transform_value(value)
        if output_record != None:
            results["values"].append(output_record)
    return json.dumps(results, ensure_ascii=False)

## Perform an operation on a record
def transform_value(value):
    try:
        recordId = value['recordId']
    except AssertionError  as error:
        return None

    # Validate the inputs
    try:         
        assert ('data' in value), "'data' field is required."
        data = value['data']        
        assert ('blob_url' in data), "'text1' field is required in 'data' object."
    except AssertionError  as error:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Error:" + error.args[0] }   ]       
            })

    try:                
        connection_string = os.environ.get('AzureBlobStorageConnectionString')
        blob_settings = {}
        settings = connection_string.split(';')
        for s in settings:
            blob_settings[s.split('=',1)[0]] = s.split('=',1)[1]

        url_parts = data['blob_url'].split('/')
        container_name = url_parts[3]
        blob_name = "/".join(url_parts[4:])
        sas_token = generate_blob_sas(
                account_name=blob_settings['AccountName'],
                container_name= container_name, 
                blob_name= blob_name,
                account_key = blob_settings['AccountKey'],
                permission="r", 
                expiry=datetime.utcnow() + timedelta(hours=3))

    except Exception as e:
        print(e.with_traceback())
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record." }   ]       
            })

    return ({
            "recordId": recordId,
            "data": {
                "file_data": {
                    "$type": "file",
                    "url" : data['blob_url'],
                    "sasToken" : sas_token
                }
                }
            })
