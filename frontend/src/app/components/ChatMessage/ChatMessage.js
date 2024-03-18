import styles from "./ChatMessage.module.css";
import { BsRobot } from "react-icons/bs";
import { FaRegUser } from "react-icons/fa";



export default function ChatMessage({ message }) {
    console.log(message)
    // for each source in the message, check if the references prop is an array or a string
    // if it's an array, map over it and return an anchor tag for each reference
    // if it's a string, return a single anchor ta

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
                                <a href={Array.isArray(source.references) ? source.references[index] : source.references} target="-blank" rel="noopener noreferrer">{source.id}</a>
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