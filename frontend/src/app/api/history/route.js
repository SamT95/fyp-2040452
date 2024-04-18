import { NextResponse } from "next/server";

// Server-side API route for submitting a message to the backend chat history API
// This route is called to populate the history sidebar with the chat history
export async function GET(req) {
    const queryParams = req.nextUrl.searchParams;
    const userId = queryParams.get("userId");
    const userName = queryParams.get("userName");
    const conversationId = queryParams.get("conversationId");
    const queryParamsString = `user_id=${userId}&conversation_id=${conversationId}`;
    const requestUrl = `${process.env.HISTORY_API_URL}/chat_history?${queryParamsString}`;
    try {
        const response = await fetch(requestUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            timeout: 30000,
            cache: "no-store",
        });
        const data = await response.json();
        return NextResponse.json({
            status: 200,
            body: {
                history: data,
            }
        });
    } catch (error) {
        console.error("Error from backend history API:", error);
        return NextResponse.json({
            status: 500,
            body: {
                message: "Failed to fetch chat history.",
                error: error
            }
        });
    }
}