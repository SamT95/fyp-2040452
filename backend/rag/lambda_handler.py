import json
from retrieval_qa_chain import create_qa_chain
import logging

# Set up logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize QA chain outside handler to leverage container reuse
#https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
chain = create_qa_chain()


def lambda_handler(event, context):
    # Extract query from API Gateway event
    logger.info("Event: %s", event)
    try:
        query = json.loads(event["body"])["query"]
    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Query parameter not found in request body"})
        }
    # Initialize and run the QA chain
    output = chain({"query": query}, return_only_outputs=True)

    result = output["result"]
    source_documents = output["source_documents"]
    logger.info("Output: %s", output)
    logger.info("Result: %s", result)


    # Return the QA chain response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "result": result,
            "source_documents": source_documents
        }),
        "headers": {
            "Content-Type": "application/json"
        }
    }
