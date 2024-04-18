"use client"
import styles from "./MessageBox.module.css";
import { useState } from "react";
import useChat from "@/app/hooks/useChat";

export default function MessageBox() {
    const [message, setMessage] = useState("");
    const { sendMessage } = useChat();

    async function handleSubmit(event) {
        event.preventDefault();

        if (!message) {
            return;
        }

        const userMessage = message;
        setMessage("");
        await sendMessage(userMessage);
    }

    function handleKeyDown(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            handleSubmit(event);
        }
    }

    return (
        <div className={styles.formContainer}>
            <form title="Message form" onSubmit={handleSubmit} className={styles.form}>
                <textarea
                id="messagetextarea" 
                onKeyDown={handleKeyDown} 
                name="message" 
                placeholder="Ask me about cyber security."
                aria-label="Message input field" 
                className={styles.textarea} 
                value={message} 
                onChange={(e) => setMessage(e.target.value)} required
                />
                <button title="Send message" role="button" name="send" type="submit" aria-label="Submit" className={styles.button}>Send</button>
            </form>
        </div>
    )
}