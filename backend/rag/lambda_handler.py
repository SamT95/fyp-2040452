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
    logger.info(f"Event: {event}")
    try:
        query = json.loads(event["body"])["query"]
    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Query parameter not found in request body"})
        }
    # Initialize and run the QA chain
    output = chain.invoke(query)
    logger.info(f"Output: {output}")


    # result = output["result"]
    # source_documents = output["source_documents"]
    # logger.info(f"Result: {result}")
    context = output["context"]
    logger.info(f"Context: {context}")
    answer = output["answer"]
    logger.info(f"Answer: {answer}")

    source_documents = [{"text": doc.page_content, "metadata": doc.metadata} for doc in context]
    logger.info(f"Source documents: {source_documents}")


    # Return the QA chain response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "result": answer,
            "source_documents": source_documents
        }),
        "headers": {
            "Content-Type": "application/json"
        }
    }
