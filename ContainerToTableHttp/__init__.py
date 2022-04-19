import logging
import os
from xml.etree.ElementInclude import include

import azure.functions as func
from azure.data.tables import TableServiceClient
from azure.storage.blob import ContainerClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Read Container name from API parameters
    container = req.params.get('container')
    if not container:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            container = req_body.get('container')

    if container:
        # Connect to Azure Table Storage
        connection_string = os.environ.get('AzureBlobStorageConnectionString') if os.environ.get('AzureBlobStorageConnectionString', None) not in (None, '') else os.environ.get('AzureWebJobsStorage')
        service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
        table_client = service_client.get_table_client(table_name=os.environ.get('TableName'))

        # List all Blobs in the container and send metadata to Azure Table Storage
        container = ContainerClient.from_connection_string(conn_str=connection_string, container_name=container)
        blob_list = container.list_blobs(include=['metadata'])
        for blob in blob_list:
            entity = {
                "PartitionKey": str(blob.container), 
                "RowKey": str(blob.name)
            }
            if blob.metadata != None:
                for key,value in blob.metadata.items():
                    entity[key] = value
            table_client.upsert_entity(entity=entity)

        return func.HttpResponse(
            f"Container {container} metadata copied on Azure Table Storage",
             status_code=200
        )

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a container name in the query string or in the request body to start a metadata dump on Azure Table Storage.",
             status_code=200
        )
