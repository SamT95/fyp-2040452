import { NextResponse } from "next/server";
import axios from "axios";


export async function POST(req) {
    // Pull the message from the request body
    const { message } = await req.json();
    // Send the message to the backend API and get a response
    try {
        const response = await axios.post(`${process.env.CHAIN_API_URL}query`, { 
            query: message
         }, {
            headers: {
                "Content-Type": "application/json",
            },
            timeout: 30000,
        });
        if (response.statusText !== "OK") {
            console.error("Error from backend API", response.data.result);
            return NextResponse.json({
                status: 500,
                body: {
                    message: response.data.result,
                }
            });
        }
        return NextResponse.json({
            status: 200,
            body: {
                message: response.data.result,
                sources: response.data.source_documents,
            }
        });
    } catch (error) {
        console.error("Error from backend API", error);
        return NextResponse.json({
            status: 500,
            body: {
                message: "Failed to submit message.",
                error: error.response.data.result,
            }
        });
    }
}