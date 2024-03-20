"use client"
import styles from "./page.module.css";
import { useState } from "react";
import useStore from "@/app/store/useStore";
import ChatContainter from "@/app/components/ChatContainer/ChatContainer";
import useChat from "@/app/hooks/useChat";
import Hero from "./components/Hero/Hero";
import Intro from "./components/Intro/Intro";

export default function Chat() {
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
      <div className={styles.pageContainer}>
        <div className={styles.heroSection}>
          <Hero />
        </div>
        <div className={styles.contentWrapper}>
          <div className={styles.introSection}>
              <Intro />
          </div>
          <div className={styles.formContainer}>
              <ChatContainter />
              <form onSubmit={handleSubmit} className={styles.form}>
                  <textarea
                  id="messagetextarea" 
                  onKeyDown={handleKeyDown} 
                  name="message" 
                  placeholder="Ask me about cyber security."
                  aria-label="Message input field." 
                  className={styles.textarea} 
                  value={message} 
                  onChange={(e) => setMessage(e.target.value)} required
                  />
                  <button type="submit" aria-label="Submit" className={styles.button}>Send</button>
              </form>
          </div>
        </div>
      </div>
    )
}