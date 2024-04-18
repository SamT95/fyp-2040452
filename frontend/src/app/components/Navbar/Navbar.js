import styles from "./Navbar.module.css";
import Link from "next/link";
import HistoryPopover from "@/app/components/HistoryPopover/HistoryPopover";

export default function Navbar() {
    return (
        <nav className={styles.navbar} role="navigation" id="navbar">
            <div className={styles.navbarContainer}>
                <h1 className={styles.navbarTitle}>
                    <Link href="/">Home</Link>
                </h1>
                <HistoryPopover />
            </div>
        </nav>
    );
}