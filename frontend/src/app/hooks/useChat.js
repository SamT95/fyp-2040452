// Hook for sending messages in the chat window
// and updating the Zustand store with the new message

import useStore from "@/app/store/useStore";
import { PulseLoader } from "react-spinners";

export default function useChat() {
    const messageId = useStore.getState().conversations.length + 1;
    const addMessage = useStore((state) => state.addMessage);
    const setLoading = useStore((state) => state.setLoading);
    const updateMessage = useStore((state) => state.updateMessage);

    async function sendMessage(messageContent) {
        // Add user message to store
        addMessage({ id: messageId, sender: "user", message: messageContent});
        setLoading(true); // Set loading state to true while waiting for response
        // Add temporaty bot loading message to store
        const loadingMessageId = messageId + 1;
        addMessage({ id: loadingMessageId, sender: "bot", message: <PulseLoader size={8}/>, loading: true});

        // Call backend API
        try {
            const response = await fetch("/api/submit", {
                method: "POST",
                body: JSON.stringify({ message: messageContent }),
                headers: {
                    "Content-Type": "application/json",
                },
            });
            const responseData = await response.json();
            const sources = responseData.body.sources;
            const sourceIdsAndReferences = sources.map(source => {
                // Some sources have a 'id' prop, whereas some have 'title'
                // we attempt to pull out both, and use the one that exists
                const id = source.metadata.id || source.metadata.title;
                const references = source.metadata.references || source.metadata.source;
                return { id, references };
            })
            const newMessage = responseData.body.message;
            updateMessage(loadingMessageId - 1, {
                message: newMessage,
                sources: sourceIdsAndReferences,
            }); // Update loading message with response
            setLoading(false); // Set loading state to false after response
        } catch (error) {
            console.error("Failed to submit message:", error);
            updateMessage(loadingMessageId - 1, {
                message: "Sorry, something went wrong. Please try again.",
            });
            setLoading(false); // Set loading state to false after response
        }
    }

    return {
        sendMessage,
    };
}
