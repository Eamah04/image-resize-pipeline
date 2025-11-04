# Image Resizing Pipeline (AWS Serverless Project)

## Overview
This project implements a **serverless image resizing pipeline** using AWS services.  
The workflow allows users to upload an image to an S3 bucket, trigger an API Gateway endpoint, and automatically resize the image through a Step Functions state machine and Lambda function.  
The resized image is then stored in a separate S3 bucket.

---

## Architecture
**Workflow:**
1. **S3 (Original Bucket)** – Stores the uploaded source image.
2. **API Gateway** – Provides a REST endpoint to trigger the pipeline.
3. **Step Functions** – Orchestrates the workflow.
4. **Lambda Function** – Resizes the image using Pillow (Python).
5. **S3 (Resized Bucket)** – Stores the resized output image.
---

## How It Works
1. Upload an image to the **original S3 bucket** (e.g., `amahoriginalimagebucket`).
2. Send a `POST` request to the API Gateway endpoint:

with JSON body:
```json
{
  "bucket": "amahoriginalimagebucket",
  "key": "Lexus350.jpg"
}
