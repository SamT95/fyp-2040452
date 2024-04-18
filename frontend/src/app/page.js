import styles from "./page.module.css";
import Hero from "./components/Hero/Hero";
import Intro from "./components/Intro/Intro";

export default function HomePage() {
    return (
      <div className={styles.pageContainer}>
        <div className={styles.heroSection}>
          <Hero />
        </div>
        <div className={styles.contentWrapper}>
          <div className={styles.introSection}>
              <Intro />
          </div>
        </div>
      </div>
    )
}