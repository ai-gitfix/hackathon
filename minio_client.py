from minio import Minio

def create_minio_client(endpoint, access_key, secret_key, secure=True):
    return Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )