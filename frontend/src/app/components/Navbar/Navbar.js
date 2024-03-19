import styles from "./Navbar.module.css";
import DeploymentStatus from "@/app/components/DeploymentStatus/DeploymentStatus";

export default function Navbar() {
    return (
        <nav className={styles.navbar} id="navbar">
            <div className={styles.navbarContainer}>
                <h1 className={styles.navbarTitle}>UP2020452 FYP</h1>
                <h1 className={styles.navbarTitle}>Cyber Security Chatbot</h1>
                <DeploymentStatus />
            </div>
        </nav>
    );
}