# Use the AWS Lambda Python 3.10 runtime as the base image
# Ensures compatibility between local deployment package and lambda runtime
FROM public.ecr.aws/lambda/python:3.10

WORKDIR /deployment

# Copy python source files into container
COPY lambda_src/ ./

COPY requirements.txt .

# Update package list and install zip
RUN yum install -y zip

# Install the function's dependencies using  requirements.txt
RUN python -m pip install -r requirements.txt --target .

# Zip the contents of the current directory (.) into a deployment package (/var/task/lambda-package.zip)
RUN zip -r9 lambda-package.zip .