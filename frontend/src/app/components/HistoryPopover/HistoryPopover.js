import { headers } from "next/headers";
import HistoryPanel from "@/app/components/HistoryPanel/HistoryPanel";


async function fetchHistory() {
    const headersStore = headers();
    // Get x-user-id and x-user-name from headers
    // (forwarded from the middleware.js file in the frontend/src directory)
    const userId = headersStore.get("x-user-id");
    const userName = headersStore.get("x-user-name");
    // If user_id or user_name is not present, return empty chat history
    if (!userId || !userName) {
        return {
            chatHistory: [],
            userId: null,
            userName: null,
        }
    }
    const conversationId = `${userName}`;
    const queryParams = `userId=${userId}&conversationId=${conversationId}`
    // Make a GET request to the history API to fetch chat history
    // providing the user_id and conversation_id as query parameters
    const response = await fetch(`${process.env.URL}/api/history?${queryParams}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        timeout: 30000,
        cache: "no-store",
    });
    const data = await response.json();
    const historyData = data.body.history;
    return {
        chatHistory: historyData,
        userId: userId,
        userName: userName,
    }
}


export default async function HistoryPopover() {
    const { chatHistory, userId, userName } = await fetchHistory();
    let chatHistories = [];
    // If chat history key is not present, set chatHistories to an empty array
    if (!chatHistory.chat_history) {
        chatHistories = [];
    } else {
        chatHistories = chatHistory.chat_history;
    }
    const chatHistoryIdentifiers = chatHistories.map((chatHistory) => {
        return {
            userId: chatHistory.user_id,
            conversationId: chatHistory.conversation_id_timestamp,
            messages: chatHistory.History,
        }
    });
    // Reverse array to sort chat history from newest to oldest
    const newestToOldestHistory = chatHistoryIdentifiers.reverse();
    return (
        <HistoryPanel history={newestToOldestHistory} userName={userName} userId={userId} />
    )
}