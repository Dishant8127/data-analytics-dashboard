import boto3
import os
from datetime import datetime
from config import Config

s3 = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION,
)

def upload_report_to_s3(manager, pdf_buffer):
    today = datetime.now().strftime("%Y-%m-%d")
    key = f"reports/{manager.region}/report_{today}.pdf"
    s3.put_object(
        Bucket=Config.AWS_S3_BUCKET,
        Key=key,
        Body=pdf_buffer.getvalue(),
        ContentType="application/pdf",
    )
    return f"https://{Config.AWS_S3_BUCKET}.s3.{Config.AWS_REGION}.amazonaws.com/{key}"
