"use client"
import useStore from "@/app/store/useStore";
import styles from "./ChatContainer.module.css";
import ChatMessage from "../ChatMessage/ChatMessage";
import PromptHint from "../PromptHint/PromptHint";
import { Prompt } from "next/font/google";
import useChat from "@/app/hooks/useChat";

export default function ChatContainer() {
    const { conversations, loading } = useStore((state) => ({ conversations: state.conversations, loading: state.loading }))
    const { sendMessage } = useChat();

    async function handleSubmit(message) {
        if (!message) {
            return;
        }

        await sendMessage(message);
    }
    return (
        <>
        <div className={styles.conversationContainer}>
            <div className={styles.messagesContainer}>
            {conversations.map((message) => {
                return (
                    <ChatMessage 
                    key={message.id} 
                    message={message} 
                />
                )
            })}
            </div>
            {conversations.length < 2 && (
                <div className={styles.promptHints}>
                    <PromptHint handleSubmit={handleSubmit} prompt="What is phishing?" />
                    <PromptHint handleSubmit={handleSubmit} prompt="What is malware?" />
                    <PromptHint handleSubmit={handleSubmit} prompt="How can malware presence be identified?" />
                </div>
            )}
        </div>
        <div className={styles.clearFloat}></div>
        </>
        
    )
}