import json
import os
import random

from minio import MinioAdmin
from minio.credentials import providers

endpoint = "upstash-storage-eu1.api.upstashdev.com"
access_key = "Yh08nykHLkGW0bA0Ou9y"
secret_key = "EpDNNMtmbMb5F36C9PwKBMWIz3aJU8aE1u5YK4GM"
secure = True

os.environ["MINIO_ACCESS_KEY"] = access_key
os.environ["MINIO_SECRET_KEY"] = secret_key
credentials = providers.EnvMinioProvider()
admin = MinioAdmin(
    endpoint=endpoint,
    secure=True,
    credentials=credentials,
)


def create_policy(username: str):
    policy = '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Action": ["s3:*"],"Resource": ["arn:aws:s3:::'+username+'-*"]}]}'
    print(policy)
    filename = f"/tmp/{username}-policy-{random.randint(0,1000)}.json"
    with open(filename, "a+") as f:
        f.write(policy)

    try:
        admin.policy_add(f"{username}-policy",filename)
    except Exception as e:
        print(e)
    print("created policy")
    return filename


def attach_policy(username: str, filepath: str):
    try:
        admin.policy_set(f"{username}-policy",username)
    except Exception as e:
        print(e)
    print("attached policy")

def create_user(username: str, secret: str):
    try:
        admin.user_add(username, secret)
        f = create_policy(username)
        attach_policy(username,f)
    except Exception as e:
        print(e)

    print("created minio user")
