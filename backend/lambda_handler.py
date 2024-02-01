import json
from retrieval_qa_chain import create_qa_chain

def lambda_handler(event, context):
    # Extract query from API Gateway event
    query = json.loads(event['body']).get('query', '')

    # Initialize and run the QA chain
    chain = create_qa_chain()
    response = chain.run({"query": query})

    # Return the QA chain response
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
