
# AWS CDK Infrastructure Directory

This folder contains the AWS CDK-based infrastructure for the project. The infrastructure is defined in Python using the [AWS Cloud Development Kit (CDK)](https://docs.aws.amazon.com/cdk/v2/guide/home.html).

## Frontend

The frontend is a dynamic Next.js-based web application that is built using Docker and deployed to AWS Fargate. The frontend is served by an AWS Application Load Balancer (ALB). The code for the frontend is located in the `frontend` folder. The CDK stack for the frontend is defined in the `frontend_stack.py` file.

## Backend

The backend infrastructure consists of a variety of components, including two AWS Lambda functions, two AWS API Gateway REST APIs, an Amazon DynamoDB table, and an Amazon Cognito user pool. The backend is defined and deployed using the AWS CDK. The code for the backend is located in the `backend` folder. The CDK stack for the backend is defined in the `backend_stack.py` file.

## Prerequisites

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```

## 
$ cdk synth
```


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

