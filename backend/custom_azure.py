from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = 'teamupblob'
    account_key = '9982y1m3zjih8wy70f+ErWDKGGMLWC37E20aHcQfgUj0yfTp8Fkwz8V+vTgC7+4eFNzCL+0I90Jvc8GTo+IPfg=='  # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None
