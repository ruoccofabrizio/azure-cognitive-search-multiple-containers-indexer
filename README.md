# Azure Blob Storage to Table Storage
This project provides two Azure Functions to copy blob metadata from Azure Blob Storage to Azure Table Storage in batch mode and event-based:
1.  BlobToTable - Function with EventGrid input to store Blob name and container name in an Azure Table Storage, using an event-based pattern
2.  ContainerToTableHttp - HTTP Function to call for copying all Blob metadata available in an Azure Blob Storage Container in an Azure Table Storage


## How to create an Event-Grid subscription for Azure Blob Storage
- [Reacting to Blob storage events](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-event-overview)
- [Use Azure Event Grid to route Blob storage events to web endpoint (Azure portal)](https://docs.microsoft.com/en-us/azure/event-grid/blob-event-quickstart-portal?toc=/azure/storage/blobs/toc.json)

## Application settings
    "AzureWebJobsStorage": # Storage account connection string for Azure Functions execution
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureBlobStorageConnectionString" : # Storage account connection string for blob metadata reading
    "TableName": "droptable" # Table Storage name for dropping metadata from blob
