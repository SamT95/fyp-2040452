"use client"
import useStore from "@/app/store/useStore";
import HistoryButton from "@/app/components/HistoryButton/HistoryButton";
import styles from "./HistoryPanel.module.css";
import { FaBars, FaTimes } from "react-icons/fa";
import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";
import Link from "next/link";

export default function HistoryPanel({ history, userName, userId }) {
    const [isHistoryOpen, setIsHistoryOpen] = useState(false);
    // Load zustand store functions and state values
    const { loadNewConversation } = useStore((state) => ({ loadNewConversation: state.loadNewConversation }));
    const { conversationId } = useStore((state) => ({ conversationId: state.conversationId }));
    const { setConversationId } = useStore((state) => ({ setConversationId: state.setConversationId }));
    const { setChatHistories } = useStore((state) => ({ setChatHistories: state.setChatHistories }));
    const { chatHistories } = useStore((state) => ({ chatHistories: state.chatHistories }));
    const { setUserId } = useStore((state) => ({ setUserId: state.setUserId }));
    const { setUserName } = useStore((state) => ({ setUserName: state.setUserName }));
    const pathname = usePathname();

    // Set userId in zustand store when userId value changes
    // or when the component mounts
    useEffect(() => {
        setUserId(userId);
        setUserName(userName);
    }, [userId]);

    // Toggle chat history panel
    function toggleHistory() {
        if (chatHistories.length === 0) {
            setChatHistories(history);
        }
        setIsHistoryOpen(!isHistoryOpen);
    }

    return (
        <aside className={`${styles.historyPanel} ${isHistoryOpen ? styles.expanded : styles.collapsed}`}>
            {/* Render chat history panel if isHistoryOpen is true */}
            {isHistoryOpen && (
                <HistoryRenderer
                loadNewConversation={loadNewConversation}
                setConversationId={setConversationId}
                chatHistories={chatHistories}
                setChatHistories={setChatHistories}
                isHistoryOpen={isHistoryOpen}
                setIsHistoryOpen={setIsHistoryOpen}
                conversationId={conversationId}
                toggleHistory={toggleHistory}
                pathname={pathname}
                userName={userName}
                userId={userId}
                />
            )}
            {/* Render open button if isHistoryOpen is false */}
            {!isHistoryOpen && (
                <button 
                type="button" 
                title="Open history" 
                aria-label="Open history" 
                className={styles.openButton} 
                onClick={toggleHistory}><FaBars /></button>
            )}
        </aside>
    )
}

function HistoryRenderer({ 
    loadNewConversation, setConversationId,
    chatHistories, setChatHistories, pathname, 
    setIsHistoryOpen, conversationId, toggleHistory,
    userName, userId
}) {
    // Create a new chat conversation in zustand
    // sets the conversation ID to associate conversation messages
    // with a new row in the backend DynamoDB table
    function handleNewChat() {
        // Generate new conversation ID based on user name and current date
        const currentDate = new Date();
        const formattedDate = `${currentDate.toDateString()} ${currentDate.toLocaleTimeString()}`
        const newConversationId = `${userName} - ${formattedDate}`;
        // Add default bot message to new conversation
        const defaultNewMessage = {
            id: 1,
            sender: "bot",
            message: "Hello! How can I help you today?",
        }
        // Load a new conversation in zustand store
        loadNewConversation([defaultNewMessage]);
        // Add new chat to chatHistories array in zustand store
        const newChat = {
            conversationId: newConversationId,
            userId: userId,
            messages: [defaultNewMessage],
        }
        setConversationId(newConversationId);
        setChatHistories([newChat, ...chatHistories]);
        // Close chat history panel after creating new chat
        setIsHistoryOpen(false);
    }
    
    return (
        <div className={styles.historyContainer}>
            <button type="button" title="Close" className={styles.closeButton} onClick={toggleHistory}><FaTimes /></button>
            <h3 className={styles.historyTitle}>Previous Chats</h3>
            { /* Render 'new chat' button and history list if the user is on the /chat page */ }
            {pathname === "/chat" ? (
                <>
                <button type="button" title="New Chat" className={styles.newChatButton} onClick={handleNewChat}>New Chat</button>
                {chatHistories.length === 0 && <p className={styles.emptyHistory}>No chat history available</p>}
                {chatHistories.map((chatHistory) => {
                    return (
                        <HistoryButton 
                        key={chatHistory.conversationId}
                        history={chatHistory}
                        active={chatHistory.conversationId === conversationId}
                        toggleHistory={() => toggleHistory(false)}
                        />
                    )
                })}
                </>
            ) : (
                <>
                { /* Render 'start chat' button if the user is not on the /chat page */ }
                <Link className={styles.chatLink} href="/chat">
                    <button type="button" title="Start Chat" className={styles.newChatButton}>Start Chat</button>
                </Link>
                <p className={styles.emptyHistory}>Chat history is only visible on the chat page.</p>
                </>
            )}
        </div>
    )
}