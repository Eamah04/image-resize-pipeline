import boto3
from io import BytesIO
from PIL import Image
import os
import urllib.parse

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Lambda triggered. Event received:")
    print(event)

    try:
        # Handle Step Function input or S3 trigger
        if 'bucket' in event and 'key' in event:
            bucket = event['bucket']
            key = event['key']
        elif 'Records' in event:
            bucket = event['Records'][0]['s3']['bucket']['name']
            raw_key = event['Records'][0]['s3']['object']['key']
            key = urllib.parse.unquote_plus(raw_key)
        else:
            raise ValueError("Event must contain either 'bucket' and 'key', or 'Records'.")

        print(f"Bucket: {bucket}, Key: {key}")
        print("Downloading image from S3...")

        # Download the image from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()

        print("Opening image with Pillow...")
        image = Image.open(BytesIO(image_data))

        print("Resizing image...")
        new_width = 500
        new_height = int(image.size[1] * (new_width / image.size[0]))
        image = image.resize((new_width, new_height))

        print("Saving resized image to memory...")
        output_stream = BytesIO()
        image.convert('RGB').save(output_stream, format="JPEG")
        output_stream.seek(0)

        # Upload the resized image back to S3
        dest_bucket = os.environ.get('RESIZED_BUCKET', '').strip()
        print("ENV RESIZED_BUCKET =", dest_bucket)
        if not dest_bucket:
            raise RuntimeError("RESIZED_BUCKET env var is not set")

        output_key = f"output/{os.path.splitext(os.path.basename(key))[0]}_resized.jpg"
        print(f"Uploading resized image to s3://{dest_bucket}/{output_key}...")
        s3.put_object(
            Bucket=dest_bucket,
            Key=output_key,
            Body=output_stream,
            ContentType='image/jpeg'
        )

        print(f"Resized image uploaded to s3://{dest_bucket}/{output_key}")

        return {
            'statusCode': 200,
            'body': f"Resized image uploaded to s3://{dest_bucket}/{output_key}"
        }

    except Exception as e:
        print("Error occurred during image processing:")
        print("Unhandled exception:", e)
        raise e
