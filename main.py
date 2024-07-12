from minio_client import create_minio_client
from user_management import add_minio_user

endpoint = "play.minio.io:9000"
admin_access_key = "Q3AM3UQ867SPQQA43P2F"
admin_secret_key = "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"

new_user_access_key = 'new_user_access_key'
new_user_secret_key = 'new_user secret'

minio_client = create_minio_client(endpoint, admin_access_key, admin_secret_key)
add_minio_user(endpoint, admin_access_key, admin_secret_key, new_user_access_key, new_user_secret_key)
