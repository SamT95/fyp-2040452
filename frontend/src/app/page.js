"use client"
import styles from "./page.module.css";
import { useState } from "react";
import useStore from "@/app/store/useStore";
import ChatContainter from "@/app/components/ChatContainer/ChatContainer";
import useChat from "@/app/hooks/useChat";

export default function Chat() {
    const [message, setMessage] = useState("");
    const { sendMessage } = useChat();

    async function handleSubmit(event) {
        event.preventDefault();

        if (!message) {
            return;
        }

        await sendMessage(message);
        setMessage("");
    }

    return (
        <div className={styles.formContainer}>
            <ChatContainter />
            <form onSubmit={handleSubmit} className={styles.form}>
                <textarea name="message" placeholder="Type your message here." className={styles.textarea} value={message} onChange={(e) => setMessage(e.target.value)} required/>
                <button type="submit" className={styles.button}>Send</button>
            </form>
        </div>
    )
}