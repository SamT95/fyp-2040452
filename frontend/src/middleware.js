import { NextResponse } from "next/server";
import { decode } from "jsonwebtoken";

export function middleware(request) {
    if (!request.cookies.has("access_token")) {
        return NextResponse.redirect(new URL("/auth", request.url));
    } else {
        const accessToken = request.cookies.get("access_token");
        const decodedToken = decode(accessToken.value); // Decode (add a check for expiration)
        const response = NextResponse.next();
        response.headers.set("user_id", decodedToken.sub);
        response.headers.set("user_name", decodedToken.username);
        response.headers.set("x-url", request.url);
        return response;
    }
}

// Specify a matcher to only apply the middleware to the /chat route
export const config = {
    matcher: "/chat"
}