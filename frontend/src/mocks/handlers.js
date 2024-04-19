import { http, HttpResponse } from "msw";

export const handlers = [
    // Chat history
    http.get(`${process.env.URL}/api/history`, ({ request }) => {
        const url = new URL(request.url);
        if (url.searchParams.get("userId") === "bob") {
            return HttpResponse.json({
                status: 500,
                error: {
                    response: {
                        data: {
                            result: "Failed to fetch chat history."
                        }
                    }
                }
            })
        } else {
            return HttpResponse.json({
                body: {
                    history: {
                        chat_history: [
                            { conversation_id_timestamp: "exampleConversationId1" },
                            { conversation_id_timestamp: "exampleConversationId2" },
                        ],
                    },
                },
            });
        }
    }),
    // API gateway URL
    http.get(`${process.env.HISTORY_API_URL}/chat_history`, ({ request }) => {
        const url = new URL(request.url);
        const userId = url.searchParams.get("user_id");
        if (userId === "bob") {
            return HttpResponse.error()
        } else {
            return HttpResponse.json({
                body: {
                    history: {
                        chat_history: [
                            { conversation_id_timestamp: "exampleConversationId1" },
                            { conversation_id_timestamp: "exampleConversationId2" },
                        ],
                    },
                },
            });
        }
    }),
];
