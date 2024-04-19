import { GET } from "@/app/api/history/route";

describe("GET /history", () => {
    it("returns a 200 status code", async () => {
        const req = {
            nextUrl: new URL("http://localhost:3000/history?userId=alice&conversationId=456")
        };
        const response = await GET(req);
        expect(response.status).toBe(200);
    });

    it("returns the chat history", async () => {
        const req = {
            nextUrl: new URL("http://localhost:3000/history?userId=alice&conversationId=456")
        };
        const response = await GET(req);
        const responseJson = await response.json();
        expect(responseJson.body.history).toBeDefined();
    });

    it("returns a 500 status code when the request fails", async () => {
        const req = {
            nextUrl: new URL("http://localhost:3000/history?userId=bob&conversationId=456")
        };
        const response = await GET(req);
        const responseJson = await response.json();
        expect(responseJson.status).toBe(500);
    });
});