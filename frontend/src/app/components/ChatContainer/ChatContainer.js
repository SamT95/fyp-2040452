"use client"
import useStore from "@/app/store/useStore";
import styles from "./ChatContainer.module.css";
import ChatMessage from "../ChatMessage/ChatMessage";

export default function ChatContainer() {
    const { conversations, loading } = useStore((state) => ({ conversations: state.conversations, loading: state.loading }))
    return (
        <>
        <div className={styles.conversationContainer}>
            {conversations.map((message) => {
                return (
                    <ChatMessage 
                    key={message.id} 
                    message={message} 
                />
                )
            })}
        </div>
        <div className={styles.clearFloat}></div>
        </>
        
    )
}