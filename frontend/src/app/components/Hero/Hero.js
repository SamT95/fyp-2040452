import styles from "./Hero.module.css";
import Button from "@/app/components/Button/Button";
import Link from "next/link";

export default function Hero() {
    return (
        <div className={styles.heroContainer}>
            <h1 className={styles.heroTitle}>Cyber Security Awareness Chatbot</h1>
            <p>A retrieval-augmented generation chatbot for cyber security knowledge and awareness</p>
            <div className={styles.heroButtons}>
                <Link href="/chat">
                    <Button variant="primary">Get started</Button>
                </Link>
                <Link href="/auth">
                    <Button variant="secondary">Register</Button>
                </Link>
            </div>
        </div>
    );
}