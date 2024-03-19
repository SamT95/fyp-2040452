import styles from "./Hero.module.css";

export default function Hero() {
    return (
        <div className={styles.heroContainer}>
            <h1 className={styles.heroTitle}>Cyber Security Awareness Chatbot</h1>
            <p>A retrieval-augmented generation chatbot for cyber security knowledge and awareness</p>
        </div>
    );
}