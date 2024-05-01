import os
import json
from google.oauth2 import service_account

# Load service account JSON from environment variable
service_account_json_str = os.getenv('SERVICE_ACCOUNT_JSON')

print(service_account_json_str)
