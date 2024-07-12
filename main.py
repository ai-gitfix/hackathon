import mimetypes
import os
from xmlrpc.client import ResponseError
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from minio import Minio, S3Error
from pydantic import BaseModel
from upstash_redis import Redis
import base64
import nanoid
from fastapi import HTTPException, status
from auth import *



app = FastAPI()
redis = Redis(
    url="https://careful-magpie-30823.upstash.io",
    token="AXhnAAIncDEwNDYzZDBiMDQ1OGI0NmM3OGZhOGFhODVhYjA5MTRkNXAxMzA4MjM",
)


ENDPOINT = "upstash-storage-eu1.api.upstashdev.com"

class RegisterData(BaseModel):
    username: str




@app.get(
    "/list_buckets",
)
def list_buckets(request: Request):
    token = request.headers.get("Authorization")
    [username, plain_pass] = get_auth(token)

    if not check_auth(username, plain_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return {"Hello": "World"}


@app.post("/register")
def register(body: RegisterData):
    if "@" in body.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid username"
        )

    password = register_user(body.username)
    if password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid username"
        )
    token = base64.b64encode(
        bytes(f"{body.username}@@{password}", encoding="utf8")
    ).decode("utf-8")
    return {"token": token}


@app.get(
    "/ls/{bucket}",
)
def listDir(request: Request, bucket: str):
    try:
        token = request.headers.get("Authorization")
        res = get_auth(token)
        if res is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        [username, plain_pass] = res
        if not check_auth(username, plain_pass):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        proxied_bucket = f"{username}-{bucket}"

        client = Minio(
            ENDPOINT, access_key=username, secret_key=get_minio_token(username)
        )
        response = client.list_objects(proxied_bucket)
        return JSONResponse({"files":[x.object_name for x in response]})
        
    except S3Error as e:
        raise HTTPException(
            status_code=404, detail=f"Bucket {bucket} not found"
        ) from e


@app.get(
    "/{bucket}/{path}",
)
def getfile(request: Request, bucket: str, path: str):
    try:
        token = request.headers.get("Authorization")
        res = get_auth(token)
        if res is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        [username, plain_pass] = res
        if not check_auth(username, plain_pass):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        proxied_bucket = f"{username}-{bucket}"

        client = Minio(
            ENDPOINT, access_key=username, secret_key=get_minio_token(username)
        )
        response = client.get_object(proxied_bucket, path)

        filename = path.split("/")[-1]
        mime_type, _ = mimetypes.guess_type(filename)

        headers = {
            "Content-Disposition": f'inline; filename="{filename}"',
            "Content-Type": mime_type or "application/octet-stream",
            "Cache-Control": "public, max-age=3600",
        }

        return StreamingResponse(response, headers=headers)
    except S3Error as e:
        raise HTTPException(
            status_code=404, detail=f"Object {path} in bucket {bucket} not found"
        ) from e

@app.post("/{bucket}")
async def upload_file(request:Request, response: JSONResponse, bucket: str, file: UploadFile = File(...)):
    try:
        response.headers["Cache-Control"] = "no-cache"
        token = request.headers.get("Authorization")
        res = get_auth(token)
        if res is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        [username, plain_pass] = res
        if not check_auth(username, plain_pass):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        proxied_bucket = f"{username}-{bucket}"

        client = Minio(
            ENDPOINT, access_key=username, secret_key=get_minio_token(username)
        )

        file_size = 0
        if file.file:
            file.file.seek(0, os.SEEK_END)
            file_size = file.file.tell()
            file.file.seek(0)
        client.put_object(
            proxied_bucket,
            file.filename,
            file.file,
            file_size,
            file.content_type,
        )
        #TODO add full url to the response
        return {"filename": file.filename, "content_type": file.content_type}
    except ResponseError as err:
        print(err)
        raise HTTPException(status_code=500, detail=f"Failed to upload")


@app.delete(
    "/{bucket}/{path}",
)
def deleteFile(request: Request, bucket: str, path: str):
    try:
        token = request.headers.get("Authorization")
        res = get_auth(token)
        if res is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        [username, plain_pass] = res
        if not check_auth(username, plain_pass):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        proxied_bucket = f"{username}-{bucket}"

        client = Minio(
            ENDPOINT, access_key=username, secret_key=get_minio_token(username)
        )
        client.remove_object(proxied_bucket, path)


        return JSONResponse(f"deleted {path} from {bucket}")
    except S3Error as e:
        print(e)
        raise HTTPException(
            status_code=404, detail=f"Object {path} in bucket {bucket} not found"
        ) from e



@app.put(
    "/{bucket}",
)
def createBucket(request: Request, bucket: str):
    try:
        token = request.headers.get("Authorization")
        res = get_auth(token)
        if res is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        [username, plain_pass] = res
        if not check_auth(username, plain_pass):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        proxied_bucket = f"{username}-{bucket}"

        client = Minio(
            ENDPOINT, access_key=username, secret_key=get_minio_token(username)
        )
        client.make_bucket(proxied_bucket)


        return JSONResponse(f"created {bucket}")
    except S3Error as e:
        print(e)
        raise HTTPException(
            status_code=404, detail=f"bucket{bucket} could not be created"
        ) from e