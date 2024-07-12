from minio_client import create_minio_client
from user_management import add_minio_user

endpoint = "upstash-storage-eu1.api.upstashdev.com"
admin_access_key = "Yh08nykHLkGW0bA0Ou9y"
admin_secret_key = "EpDNNMtmbMb5F36C9PwKBMWIz3aJU8aE1u5YK4GM"

new_user_access_key = 'new_user_access_key'
new_user_secret_key = 'new_user secret'

minio_client = create_minio_client(endpoint, admin_access_key, admin_secret_key)
add_minio_user(endpoint, admin_access_key, admin_secret_key, new_user_access_key, new_user_secret_key)
