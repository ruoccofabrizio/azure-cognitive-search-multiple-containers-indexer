import json
import logging
import os

import azure.functions as func
from azure.data.tables import TableServiceClient
from azure.storage.blob import BlobClient


def main(event: func.EventGridEvent):
    # Get Event Grid data
    data = event.get_json()

    # Connect to Azure Table Storage
    connection_string = os.environ.get('AzureBlobStorageConnectionString') if os.environ.get('AzureBlobStorageConnectionString', None) not in (None, '') else os.environ.get('AzureWebJobsStorage')
    service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = service_client.get_table_client(table_name=os.environ.get('TableName'))

    # Define PartitionKey = container name and Row_Key as file name
    partition_key = event.subject.split('/')[4]
    row_key = "/".join(event.subject.split('/')[6:])

    # Delete entry in the table if the Blob is deleted, add a row otherwise
    if data['api'] == 'DeleteBlob':
        table_client.delete_entity(row_key=row_key, partition_key=partition_key)
    else:
        entity = {
            "PartitionKey": partition_key, 
            "RowKey": row_key,
            "Url": data['url']
        }
        if int(os.environ.get('CopyMetadata', 0)) == 1:
            blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=partition_key, blob_name=row_key)
            metadata = blob.get_blob_properties()['metadata']
            if metadata != None:
                for key, value in metadata.items():
                    entity[key] = value
        table_client.upsert_entity(entity=entity)
