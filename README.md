# UP2040452 Final Year Project

This repository stores the code utilised in my final year project. This is a monorepo containing backend, frontend and infrastructure code.

## Table of Contents
- [Frontend](#frontend)
    - [Server-side Frontend Actions](#server-side-frontend-actions)
    - [Server-side API Route Handlers](#server-side-api-route-handlers)
    - [Unit Tests](#unit-tests)
- [Backend](#backend)
- [Deployment](#deployment)
    - [Lambda Deployment Package](#lambda-deployment-package)
    - [AWS CDK](#aws-cdk)
    - [User Authentication](#user-authentication)

## Frontend
The `frontend/` folder contains the source code of the frontend utilised in the project. The frontend was created using [Next.js](https://nextjs.org/) and [React](https://react.dev/).

All styling is done using CSS3 and is fully custom. The frontend is accessible and responsive and can be viewed on any device.

### Server-side Frontend Actions
Next.js provides a feature called [server actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations) that allows you to run code on the server side before rendering a page. This was utilised when interacting with AWS Cognito via the AWS SDK. The server actions are defined in the `frontned/src/app/actions/` directory.

### Server-side API Route Handlers
Next.js also provides a feature called [API routes](https://nextjs.org/docs/api-routes/introduction) that allows you to create server-side endpoints that can be called from the frontend. This was utilised when interacting with the backend API Gateway endpoints. The API route handlers are defined in the `frontend/src/app/api/` directory.

### Unit Tests
Unit tests for the frontend components are written using [Jest](https://jestjs.io/) and [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/). The tests are defined in the `frontend/src/app//__tests__/` directory. The [Mock Service Worker](https://mswjs.io/) library is utilised to mock the API requests made by the frontend components. MSW mocks can be found in the `frontend/src/mocks/` directory. The tests can be run using the `npm run test` command. The Jest configuration can be found in the `frontend/jest.config.js` file, alongside helper files like `jest.polyfills.js` and `jest.setup.js`. 

## Backend
The `backend/` folder contains the source code of the backend utilised in the project. The backend was created using [Python](https://www.python.org/).

### Retrieval-Augmented Generation Chain
The backend code is responsible for creating and managing the retrieval-augmented generation chain. The chain consists broadly of the following components:

- A [DynamoDB](https://aws.amazon.com/dynamodb/) table that stores the chat history.
- A [Lambda](https://aws.amazon.com/lambda/) function that serves as the entrypoint for the retrieval-augmented generation chain.
- An [API Gateway](https://aws.amazon.com/api-gateway/) that serves as the interface between the frontend and the chain Lambda function.
- A [Pinecone vector store](https://www.pinecone.io/) that stores the embeddings of the chat history.
- The [Cohere embed english v3.0](https://cohere.com/) embedding model that generates embeddings for user queries and fetched data.
- The [Hugging Face Transformers](https://huggingface.co/transformers/) library that deploys the [Mistral-7B-Instruct-v0.1 LLM](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1) to [Amazon SageMaker](https://aws.amazon.com/sagemaker/).

### Data Fetching and Ingestion
The backend code is also responsible for fetching and ingesting data from various sources. The data fetching and ingestion components are defined in the `backend/scraper/` and `backend/vevtorisation/` directories. The `backend/scraper_coordinator.py` file coordinates the fetching and ingestion of data from various sources. The `backend/scraper/` directory contains the code for fetching data and the `backend/vectorisation/` directory contains the code for creating embeddings for the fetched data.

The sources of data are defined below:

- [CyBOK](https://www.cybok.org/) - The Cybersecurity Body of Knowledge (CyBOK) is a comprehensive body of knowledge that focuses on cyber security. The combined CyBOK PDF is fetched and processed before being embedded and stored.
- [CVE Database](https://cve.mitre.org/) - The Common Vulnerabilities and Exposures (CVE) database is a publicly available list of common vulnerabilities and exposures. The [CVElist GitHub Repository](https://github.com/CVEProject/cvelistV5/) published scheduled JSON files containing new and updated CVEs. These files are fetched and processed before being embedded and stored.
- [CISA Alerts](https://www.cisa.gov/news-events/cybersecurity-advisories) - The Cybersecurity and Infrastructure Security Agency (CISA) publishes alerts on their website. The alerts are fetched and processed before being embedded and stored.

### Automated Data Fetching
The backend code is responsible for automatically fetching and ingesting data from the sources mentioned above. The data fetching and ingestion components are defined in the `backend/scraper/` and `backend/vectorisation/` directories. The `backend/scraper_coordinator.py` file coordinates the fetching and ingestion of data from various sources. The `backend/scraper_coordinator.py` file is run every 24 hours using a scheduled [GitHub Actions](https://docs.github.com/en/actions) workflow. The workflow can be found in the `.github/workflows/scheduled_data_fetching.yml` file.


## Deployment
Deployment of both the frontend and backend components (defined in the `infra/` directory) is done using the [AWS Cloud Development Kit (CDK)](https://aws.amazon.com/cdk/). The CDK code is written in Python and can be found in the `infra/` directory.

Deployments are automated using [GitHub Actions](https://docs.github.com/en/actions). The deployment workflows can be found in the `.github/workflows/` directory. The workflows are triggered on pushes to the `main` branch.

The frontend deployment workflow, defined in `.github/workflows/deploy_frontend.yml`, builds the frontend Docker image, pushes it to the Elastic Container Registry (ECR), and updates the ECS service with the new image. This workflow is triggered when changes are made to the `frontend/` directory.

The backend deployment workflow, defined in `.github/workflows/deploy_backend.yml`, deploys the backend infrastructure using the CDK. This workflow is triggered when changes are made to the `backend/` directory.

### Lambda Deployment Package
The code in the `backend` folder has various functions, such as setting fetching and ingesting data, creating embeddings, deploying LLMs to SageMaker, and so on. While functions related to data ingestion and data embedding only need to run periodically, the functions that initialise and query the retrieval QA chain will need to run for each user query. 

To enable this, AWS' serverless Lambda functions are utilised. The code in `backend/rag/lambda_handler.py` server as the entrypoint, or handler, of the lambda function. The handler accepts parameters in the form of an event and queries the chain with the supplied data. 

To deploy the backend code, and to ensure that all dependencies utilised in the backend code are available, the [`aws_lambda_python_alpha`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-lambda-python-alpha-readme.html) library is used. This construct will handle installing all required modules (using a `requirements.txt` or other requirement file) in a Lambda-compatible Docker container.

### AWS CDK
The [AWS Cloud Development Kit](https://aws.amazon.com/cdk/) for Python was utilised to define the infrastructure components as code for this project. The infrastructure code can be found in the `infra/` directory.

Individual [AWS CloudFormation stacks](https://aws.amazon.com/cloudformation/) are created for the frontend and backend infrastructure components. The CDK code definitions for the frontend can be found in `infra/frontend` and the definitions for the backend components can be found in `infra/backend`.

The CDK code for the backend infrastructure components is responsible for creating the following resources:

- An AWS Lambda function that will serve as the entrypoint for the retrieval-augmented generation chain.
    - An AWS API Gateway that will serve as the interface between the frontend and the chain Lambda function.
    - The lambda handler code is stored in the `backend/rag/lambda_handler.py` file.
- An AWS Lambda function that will serve as the entrypoint for querying the DynamoDB chat history table.
    - An AWS API Gateway that will serve as the interface between the frontend and the history Lambda function.
    - The lambda handler code is stored in the `backend/chat_history/lambda_handler.py` file.
- An AWS DynamoDB table that will store the chat history.
- An AWS Cognito User Pool that will manage user authentication.
- An AWS Cognito app client that will allow the frontend to authenticate users.
- Various IAM roles and policies that will allow the Lambda functions to interact with other AWS services.
    - For example, the query chain Lambda function will need permission to read and write to the DynamoDB table.
    - The chat history Lambda function will need permission to read from the DynamoDB table.

The CDK code for the frontend infrastructure components is responsible for creating the following resources:

- An AWS Elastic Container Registry (ECR) repository that will store the frontend Docker container.
- An AWS Elastic Container Service (ECS) cluster that will host the frontend Docker container.
    - An AWS Fargate service and task definition that will run the frontend Docker container.
    - An AWS Application Load Balancer that will route traffic to the Fargate service.
- An AWS Route 53 hosted zone that will manage the domain name for the frontend.
    - An AWS Certificate Manager certificate that will secure the domain name with HTTPS.
- Various security groups and VPC endpoints that will allow the frontend to interact with the backend services, without requiring public IPs.

### User Authentication
User authentication is handled using [Amazon Cognito](https://aws.amazon.com/cognito/). Amazon Cognito provides user pools that manage user sign-up, sign-in, and access control for web and mobile applications. The CDK code in `infra/backend/backend_stack.py` defines a Cognito user pool and app client that will be used to authenticate users of the frontend.

[Next.js server actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations) are utilised to handle user authentication in the frontend. When a user signs in, the frontend sends the user's credentials to the Cognito user pool, which returns an access token, ID token and refresh token. The frontend stores these tokens in HTTP-only cookies and sends the access token with each request to the backend [AWS API Gateway](https://aws.amazon.com/api-gateway/) APIs. The backend API verifies the token with the Cognito user pool and returns the requested data if the token is valid. The server actions are defined in the `frontend/actions/` directory. Since these actions run on the server side, they can access the HTTP-only cookies and securely manage user authentication.