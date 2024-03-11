# Use the AWS Lambda Python 3.10 runtime as the base image
# Ensures compatibility between local deployment package and lambda runtime
FROM public.ecr.aws/lambda/python:3.10

WORKDIR /lambda_dependencies

# Copy requirements.txt for files to be deployed on Lambda
COPY requirements.txt .

# Install the function's dependencies using requirements.txt
# The --target option specifies the directory to store the installed packages,
# which is set to the Python packages directory used by AWS Lambda.
RUN python -m pip install -r requirements.txt --target /var/task/python