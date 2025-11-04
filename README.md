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

   [Client/Postman] → [API Gateway] → [Step Functions] → [Lambda] → [S3 Resized Bucket] ↑ └── [S3 Original Bucket]
---

## How It Works
1. Upload an image to the **original S3 bucket** (e.g., `amahoriginalimagebucket`).
2. Send a `POST` request to the API Gateway endpoint:https://<api-id>.execute-api.<region>.amazonaws.com/trigger

with JSON body:
```json
{
  "bucket": "amahoriginalimagebucket",
  "key": "Lexus350.jpg"
}

----
3. API Gateway starts the Step Functions state machine.

4. Step Functions invokes the Lambda function.

5. Lambda fetches the image, resizes it, and saves it to the resized bucket (e.g., amahresizedimagebucket).

6. The resized image can be retrieved from the resized bucket.

## Testing the Pipeline
Step 1: Upload an image to the original S3 bucket.
Step 2: Use Postman to send a POST request with Content-Type: application/json. Example body:
{
  "bucket": "amahoriginalimagebucket",
  "key": "Lexus350.jpg"
}
Step 3: Verify execution in the Step Functions console.

Step 4: Check the resized S3 bucket for the output image.

## Source Code
Lambda function: lambda/lambda_function.py
Step Functions definition: stepfunctions/state_machine.json

## Author
Emmanuel Amah
Registered Nurse | Business Information Systems Student | Aspiring Cloud & Systems Develope
