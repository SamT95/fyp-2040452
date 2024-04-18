import styles from "./Footer.module.css";
import { FaExternalLinkAlt } from "react-icons/fa";

export default function Footer() {
    return (
        <div className={styles.footerContainer}>
            <p>Sam Thompson / UP2040452 FYP</p>
            <a className={styles.githubLink} href="https://github.com/SamT95/fyp-2040452" target="_blank" rel="noopener noreferrer">
                GitHub
                <FaExternalLinkAlt />
            </a>
        </div>
    );
}