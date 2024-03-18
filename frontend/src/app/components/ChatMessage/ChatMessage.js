import styles from "./ChatMessage.module.css";

export default function ChatMessage({ message }) {
    return (
        <div className={message.sender === "bot" ? styles.botMessageContainer : styles.userMessageContainer}>
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
        </div>
    )
}