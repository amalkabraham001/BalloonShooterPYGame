#!/bin/bash

# Replace with your S3 bucket name
BUCKET_NAME="your-bucket-name"

# Upload files to S3
aws s3 cp index.html s3://$BUCKET_NAME/
aws s3 cp style.css s3://$BUCKET_NAME/
aws s3 cp game.js s3://$BUCKET_NAME/

# Set public read permissions
aws s3api put-object-acl --bucket $BUCKET_NAME --key index.html --acl public-read
aws s3api put-object-acl --bucket $BUCKET_NAME --key style.css --acl public-read
aws s3api put-object-acl --bucket $BUCKET_NAME --key game.js --acl public-read

echo "Game deployed to http://$BUCKET_NAME.s3-website-us-east-1.amazonaws.com/"
echo "Note: You may need to configure your bucket for static website hosting in the AWS console"