import styles from "./ChatMessage.module.css";
import { BsRobot } from "react-icons/bs";
import { FaRegUser } from "react-icons/fa";

export default function ChatMessage({ message }) {
    return (
        <div aria-live="polite" aria-label="Chat message" className={message.sender === "bot" ? styles.botMessageContainer : styles.userMessageContainer}>
            {message.sender === "bot" ? <div className={styles.botIcon}><BsRobot aria-label="Bot icon" role="img" /></div> : null }
            <div className={message.sender === "bot" ? styles.botMessage : styles.userMessage}>
                <p>
                    {message.message}
                </p>
                {message.sources && (
                <div className={styles.sourceContainer}>
                    <h4 id="sourceHeading">Sources:</h4>
                    <ul aria-labelledby="sourceHeading" className={styles.sourceList}>
                        {message.sources.map((source, index) => (
                            <li key={index} className={styles.sourceItem}>
                                <a className={styles.sourceLink} 
                                href={Array.isArray(source.references) ? source.references[index] : source.references} target="-blank" rel="noopener noreferrer">
                                    {source.id}
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
            </div>
            {message.sender === "user" ? <div className={styles.userIcon}><FaRegUser aria-label="User icon" role="img"/></div> : null }
        </div>
    )
}