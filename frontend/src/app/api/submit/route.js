import { NextResponse } from "next/server";

export async function POST(req) {
    // Pull the message from the request body
    const { message } = await req.json();
    // Send the message to the backend API and get a response
    try {
        console.log("Testing env var:", process.env.CHAIN_API_URL);
        const response = await fetch(`${process.env.CHAIN_API_URL}query`, {
            method: "POST",
            body: JSON.stringify({ query: message }),
            headers: {
                "Content-Type": "application/json",
            },
        });
        const data = await response.json();
        console.log("Response data from backend API", data)
        if (data.message) {
            console.error("Error from backend API", data.message);
            return NextResponse.json({
                status: 500,
                body: {
                    message: data.message,
                }
            });
        }
        return NextResponse.json({
            status: 200,
            body: {
                message: data.result,
                sources: data.source_documents,
            }
        });
    } catch (error) {
        console.error("Error from backend API", error);
        return NextResponse.json({
            status: 500,
            body: {
                message: "Failed to submit message.",
                error: error.message,
            }
        });
    }
}