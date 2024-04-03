import boto3
import json
from boto3.dynamodb.conditions import Key
import os

table_name = os.environ["TABLE_NAME"]
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Extract user ID and conversation ID from query string parameters
    try:
        user_id = event["queryStringParameters"]["user_id"]
        conversation_id = event["queryStringParameters"]["conversation_id"]
    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "User ID or conversation ID not found in query string parameters"})
        }
    
    # Retrieve chat history from DynamoDB
    response = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id) & Key("conversation_id_timestamp").begins_with(conversation_id)
    )

    items = response.get("Items", [])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "chat_history": items
        }),
        "headers": {
            "Content-Type": "application/json"
        }
    }
