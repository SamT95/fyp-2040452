import { NextResponse } from "next/server";
import AWS from "aws-sdk";

export async function GET() {
    // Pull the message from the request body
    const sageMaker = new AWS.SageMaker({
        region: "eu-west-1",
    })

    try {
        const endpointStatus = await sageMaker.describeEndpoint({
            EndpointName: "huggingface-rag-llm-endpoint",
        }).promise();

        if (endpointStatus.EndpointStatus !== "InService") {
            return NextResponse.json({
                status: 500,
                body: {
                    message: "SageMaker endpoint is not in service",
                }
            });
        } else {
            return NextResponse.json({
                status: 200,
                body: {
                    message: "SageMaker endpoint is in service",
                }
            });
        }
    } catch (error) {
        console.error("Error from SageMaker", error);
        return NextResponse.json({
            status: 500,
            body: {
                message: "Failed to check endpoint status.",
                error: error.message,
            }
        });
    }
}