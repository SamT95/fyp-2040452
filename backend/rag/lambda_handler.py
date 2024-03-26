import json
from retrieval_qa_chain import create_qa_chain
from langchain_core.messages import HumanMessage
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
    chat_history = []
    try:
        query = json.loads(event["body"])["query"]
    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Query parameter not found in request body"})
        }
    # Initialize and run the QA chain
    # output = {}
    # current_key = None
    # for chunk in chain.stream(query):
    #     for key in chunk:
    #         if key in output:
    #             output[key] += chunk[key]
    #         else:
    #             output[key] = chunk[key]
    #         if key != current_key:
    #             logger.info(f"{key}: {chunk[key]}")
    #         else:
    #             logger.info(f"Chunk: {chunk[key]}")
    #         current_key = key
    output = chain.invoke({"question": query, "chat_history": chat_history})
    chat_history.extend([HumanMessage(content=query), output])
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
