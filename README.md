# Indexing multiple Azure Blob Storage containers in Azure Cognitive Search 
This repo provides an example on how to index multiple [Azure Blob Storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-overview) containers in [Azure Cognitive Search](https://docs.microsoft.com/en-us/azure/search/search-what-is-azure-search) by using a single [Azure Table Storage Indexer](https://docs.microsoft.com/en-us/azure/search/search-howto-indexing-azure-tables) and dumping blob metadata in an [Azure Table Storage](https://docs.microsoft.com/en-us/azure/storage/tables/table-storage-overview) with [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-overview).

![Skillset](/images/skillset.png)

Logical components:
-   Generate SAS: Azure Functions to [generate a SAS token](https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob?view=azure-python) from an Azure Blob URL. It returns a file reference accordingly to Document Extraction skill format
-   Document Cracking: Uses the Azure Cognitive Search [Document Extraction skill](https://docs.microsoft.com/en-us/azure/search/cognitive-search-skill-document-extraction) to crack different [supported document formats](https://docs.microsoft.com/en-us/azure/search/cognitive-search-skill-document-extraction#supported-document-formats)
-   [Key Phrase Extraction](https://docs.microsoft.com/en-us/azure/search/cognitive-search-skill-keyphrases): A skill that uses the text extracted by the Document Cracking skill. You can add any other [pre-builthttps://docs.microsoft.com/en-us/azure/search/cognitive-search-predefined-skills] or [custom skill](https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-web-api) here

Azure Cognitive Search assets:
-   [Data Source](./datasource.json)
-   [Index](./index.json)
-   [Indexer](./indexer.json)
-   [Skillset](./skillset.json)

## Azure Blob Storage to Table Storage
The project provides two Azure Functions to copy blob metadata from Azure Blob Storage to Azure Table Storage in batch mode and event-based:
1.  BlobToTable - Function with EventGrid input to store Blob name and container name in an Azure Table Storage, using an event-based pattern
2.  ContainerToTableHttp - HTTP Function to call for copying all Blob metadata available in an Azure Blob Storage Container in an Azure Table Storage
Use the batch mode for the initial ingestion and the event-based function to keep consistency between the updated blobs and the rows in the Azure Table Storage.


## How to create an Event-Grid subscription for Azure Blob Storage
- [Reacting to Blob storage events](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-event-overview)
- [Use Azure Event Grid to route Blob storage events to web endpoint (Azure portal)](https://docs.microsoft.com/en-us/azure/event-grid/blob-event-quickstart-portal?toc=/azure/storage/blobs/toc.json)

## Application settings
    "AzureWebJobsStorage": # Storage account connection string for Azure Functions execution
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureBlobStorageConnectionString" : # Storage account connection string for blob metadata reading and SAS Token generation
    "TableName": "droptable" # Table Storage name for dropping metadata from blob
    "CopyMetadata": # set to "1" if you want to copy Blob Metadata in the event-based function (BlobToTable)
