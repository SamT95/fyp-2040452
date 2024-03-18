import styles from "./ChatMessage.module.css";
import { BsRobot } from "react-icons/bs";
import { FaRegUser } from "react-icons/fa";



export default function ChatMessage({ message }) {
    return (
        <div className={message.sender === "bot" ? styles.botMessageContainer : styles.userMessageContainer}>
            {message.sender === "bot" ? <div className={styles.botIcon}><BsRobot /></div> : null }
            <div className={message.sender === "bot" ? styles.botMessage : styles.userMessage}>
                <p>
                    {message.message}
                </p>
                {message.sources && (
                <div className={styles.sourceContainer}>
                    <h4>Sources:</h4>
                    <ul className={styles.sourceList}>
                        {message.sources.map((source, index) => (
                            <li key={index} className={styles.sourceItem}>
                                <a href={source.references[index]} target="-blank" rel="noopener noreferrer">{source.id}</a>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
            </div>
            {message.sender === "user" ? <div className={styles.userIcon}><FaRegUser /></div> : null }
        </div>
    )
}