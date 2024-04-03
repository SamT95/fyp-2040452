import json
from retrieval_qa_chain import create_qa_chain
from langchain_core.messages import HumanMessage
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
import logging
import os

# Set up logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize QA chain outside handler to leverage container reuse
#https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
table_name = os.environ["TABLE_NAME"]


def lambda_handler(event, context):
    # Extract query from API Gateway event
    logger.info(f"Event: {event}")
    try:
        body = json.loads(event["body"])
        query = body["query"]
        user_id = body["user_id"]
        conversation_id = body.get("conversation_id", "default")
    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Query parameter not found in request body"})
        }
    
    # Initialize the QA chain
    chain = create_qa_chain(table_name=table_name, session_id=user_id)
    
    # Retrieve chat history from DynamoDB
    chat_history = DynamoDBChatMessageHistory(table_name=table_name, session_id=user_id)

    logger.info(f"Chat history: {chat_history}")
    logger.info(f"Conversation ID: {conversation_id}")

    # Initialize and run the QA chain
    output = chain.invoke(
        {"question": query},
        config={"configurable": {"session_id": user_id}},
    )
    logger.info(f"Output: {output}")
    answer = output["content"]
        

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
