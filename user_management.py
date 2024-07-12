import requests
import json

def add_minio_user(endpoint, admin_access_key, admin_secret_key, new_user_access_key, new_user_secret_key):
    admin_api_url = f"https://{endpoint}/minio/admin/v3/add-user"

    new_user = {
        "accessKey": new_user_access_key,
        "secretKey": new_user_secret_key
    }

    try:
        response = requests.post(
            admin_api_url,
            headers={"Content-Type": "application/json"},
            auth=(admin_access_key, admin_secret_key),
            data=json.dumps(new_user)
        )
        if response.status_code == 200:
            print("User added successfully")
        else:
            print(f"Error adding user: {response.text}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")


def list_minio_users(endpoint, admin_access_key, admin_secret_key):
    admin_api_url = f"https://{endpoint}/minio/admin/v3/list-users"

    try:
        response = requests.get(
            admin_api_url,
            headers={"Content-Type": "application/json"},
            auth=(admin_access_key, admin_secret_key)
        )

        if response.status_code == 200:
            users = response.json()
            print("Users:", users)
            return users
        else:
            print(f"Error listing users: {response.text}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

def get_minio_user_info(endpoint, admin_access_key, admin_secret_key, user_access_key):
    admin_api_url = f"https://{endpoint}/minio/admin/v3/user-info?accessKey={user_access_key}"

    try:
        response = requests.get(
            admin_api_url,
            headers={"Content-Type": "application/json"},
            auth=(admin_access_key, admin_secret_key)
        )

        if response.status_code == 200:
            user_info = response.json()
            print("User Info:", user_info)
            return user_info
        else:
            print(f"Error getting user info: {response.text}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")


def update_minio_user_policy(endpoint, admin_access_key, admin_secret_key, user_access_key, policy_name):
    admin_api_url = f"https://{endpoint}/minio/admin/v3/set-user-policy"

    data = {
        "accessKey": user_access_key,
        "policyName": policy_name
    }

    try:
        response = requests.put(
            admin_api_url,
            headers={"Content-Type": "application/json"},
            auth=(admin_access_key, admin_secret_key),
            data=json.dumps(data)
        )

        if response.status_code == 200:
            print(f"Policy '{policy_name}' set for user '{user_access_key}' successfully")
        else:
            print(f"Error setting policy: {response.text}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

