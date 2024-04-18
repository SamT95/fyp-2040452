"use client"
import useStore from "@/app/store/useStore";
import styles from "./HistoryButton.module.css";
import { FaHistory } from "react-icons/fa";

export default function HistoryButton({ history, active, toggleHistory }) {
    const { loadNewConversation } = useStore((state) => ({ loadNewConversation: state.loadNewConversation }));
    const { setConversationId } = useStore((state) => ({ setConversationId: state.setConversationId }));
    // Split conversationId to the username and date
    const splitConversationIdDate = history.conversationId.split(" - ");
    const userName = splitConversationIdDate[0];
    const conversationDate = splitConversationIdDate[1];

    function handleClick() {
        // Load chat history into zustand store
        // when a chat history button is clicked
        const messages = history.messages;
        const formattedMessages = messages.map((message, index) => {
            return {
                id: index,
                sender: message.data.type === "ai" ? "bot" : "user",
                message: message.data.content,
            }
        });
        setConversationId(history.conversationId);
        loadNewConversation(formattedMessages);
        toggleHistory();
    }

    return (
        <button title="Load chat"
        className={`${styles.historyButton} ${active ? styles.active : ""}`}
        onClick={handleClick}
        >
            <div className={styles.historyId}>
                <p>{userName}</p>
                <p>{conversationDate}</p> 
            </div>
            <FaHistory />
        </button>
    )
}