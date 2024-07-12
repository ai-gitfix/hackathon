import base64
import string
import nanoid
from upstash_redis import Redis
from passlib.context import CryptContext

import minio_admin



redis = Redis(
    url="https://careful-magpie-30823.upstash.io",
    token="AXhnAAIncDEwNDYzZDBiMDQ1OGI0NmM3OGZhOGFhODVhYjA5MTRkNXAxMzA4MjM",
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_username_key(username):
    return "user:" + username


def get_auth(token: str):
    bearer_const = "Bearer "
    if token is None or not token.startswith(bearer_const):
        return None
    token = token.split(bearer_const)[1]
    try:
        decoded = base64.b64decode(token.encode("utf8")).decode("utf8").split("@@")
        if len(decoded) != 2:
            return None
        [username, password] = decoded

    except Exception as e:
        print(e)
        return None

    return username, password


def check_auth(username, plain_password):
    hashed_password = redis.hget(get_username_key(username), "password")
    if hashed_password is None:
        return False
    return pwd_context.verify(plain_password, hashed_password)


def get_minio_token(username):
    password_key = "password"
    return redis.hget(get_username_key(username), password_key)


def register_user(username):
    password_key = "password"
    if redis.hget(get_username_key(username), password_key) != None:
        return None

    password = str(nanoid.generate(size=30, alphabet=string.ascii_letters))
    hashed_password = pwd_context.hash(password)

    minio_admin.create_user(username, hashed_password)

    redis.hset(get_username_key(username), password_key, hashed_password)
    return password
