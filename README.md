# UP2040452 Final Year Project

This repository stores the code utilised in my final year project. This is a monorepo containing both backend and frontend code.

## Table of Contents
- [Frontend](#frontend)
- [Backend](#backend)
    - [Libraries Utilised](#libraries-utilised)
    - [Data Ingestion](#data-ingestion)
    - [Creating and Storing Embeddings](#creating-and-storing-embeddings)
    - [Context Retrieval and Reranking](#context-retrieval-and-reranking)
    - [Model Selection](#model-selection)

## Frontend
The `frontend/` folder contains the source code of the frontend utilised in the project. The frontend was created using [Next.js](https://nextjs.org/) and [React](https://react.dev/).

All styling is done using CSS3 and is fully custom. 

The frontend is a WIP. It aims to provide an interface between a user visiting the site and the retrieval augmented generation chain running on the backend.

## Backend
The `backend/` folder contains the source code of the backend utilised in the project. The backend was created using [Python](https://www.python.org/)

### Libraries Utilised
Below is a list of the Python libraries utilised in the backend and the justification for their usage.

### Data Ingestion
WIP

### Creating and Storing Embeddings
WIP

### Context Retrieval and Reranking
WIP

### Model Selection
WIP

### Deployment

#### Lambda Deployment Package
The code in the `backend` folder has various functions, such as setting fetching and ingesting data, creating embeddings, deploying LLMs to SageMaker, and so on. While functions related to data ingestion and data embedding only need to run periodically, the functions that initialise and query the retrieval QA chain will need to run for each user query. 

To enable this, AWS' serverless Lambda functions are utilised. The code in `backend/rag/lambda_handler.py` server as the entrypoint, or handler, of the lambda function. The handler accepts parameters in the form of an event and queries the chain with the supplied data. 

To deploy the backend code, and to ensure that all dependencies utilised in the backend code are available, the [`aws_lambda_python_alpha`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-lambda-python-alpha-readme.html) library is used. This construct will handle installing all required modules (using a `requirements.txt` or other requirement file) in a Lambda-compatible Docker container.

#### AWS CDK
WIP