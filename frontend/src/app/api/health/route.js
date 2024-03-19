import { NextResponse } from "next/server";

export async function GET() {
    console.log("Health check")
    return NextResponse.json({
        status: 200,
    });
}