import boto3
from botocore.client import Config
import time
from werkzeug.utils import secure_filename
import os


class FileStorageService:
    def __init__(self):
        self.bucket_name = os.environ.get("R2_BUCKET_NAME")
        self.account_id = os.environ.get("R2_ACCOUNT_ID")
        self.access_key = os.environ.get("R2_ACCESS_KEY_ID")
        self.secret_key = os.environ.get("R2_SECRET_ACCESS_KEY")
        self.public_base_url = "https://pub-441dc43623a443b28be57c3c2e511876.r2.dev"
        
        if not all([self.bucket_name, self.account_id, self.access_key, self.secret_key]):
            raise ValueError("Faltan credenciales de R2 en las variables de entorno")
            
        self.client = boto3.client(
            "s3",
            region_name = "auto",
            endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com",
            aws_access_key_id = self.access_key,
            aws_secret_access_key = self.secret_key,
            config = Config(signature_version = "s3v4")
        )

    def save(self, image):
        
        #set an unique filename
        original_name = secure_filename(image.filename)
        timestamp = int(time.time())
        filename = f"{timestamp}_{original_name}"
        
        # uploads the file
        self.client.upload_fileobj(image, self.bucket_name, filename)
        
        #builds the filepath
        #filepath = f"https://{self.bucket_name}.{self.account_id}.r2.cloudflarestorage.com/{filename}"
        
        return filename
        
