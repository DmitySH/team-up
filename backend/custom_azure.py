from storages.backends.azure_storage import AzureStorage

import config.secrets_azure as az_secret


class AzureMediaStorage(AzureStorage):
    account_name = 'teamupblob'
    account_key = az_secret.AZURE_KEY
    azure_container = 'media'
    expiration_secs = None
