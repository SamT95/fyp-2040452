import styles from "./Intro.module.css";
import { FaCheckCircle, FaBan } from "react-icons/fa";

export default function Intro() {

    const sourcesAndLinks = [
        {
            source: "Common Vulnerabilities and Exposures (CVE) database",
            link: "https://cve.mitre.org/"
        },
        {
            source: "Cyber Security Body of Knowledge (CyBOK) PDFs",
            link: "https://www.cybok.org/"
        },
        {
            source: "Cyber Security Alerts & Advisories",
            link: "https://www.cisa.gov/news-events/cybersecurity-advisories"
        },
        {
            source: "Security blogs and news articles",
            link: "https://www.zdnet.com/topic/security/"
        },
        {
            source: "Security vendor advisories",
            link: "https://www.cisco.com/c/en/us/support/security/index.html"
        }
    ]

    const additionalSourcesAndLinks = [
        {
            source: "NCSC Cyber Security Guidance",
            link: "https://www.ncsc.gov.uk/section/advice-guidance/all-topics"
        },
        {
            source: "NIST Cyber Security Guidance",
            link: "https://www.nist.gov/cybersecurity"
        },
        {
            source: "Cyber Aware Campaign",
            link: "https://www.ncsc.gov.uk/cyberaware/home"
        },
        {
            source: "Cyber Essentials Scheme",
            link: "https://www.ncsc.gov.uk/cyberessentials/overview"
        }
    ]

    return (
        <div className={styles.introContainer}>
            <div className={styles.introInfo}>
                <h1 className={styles.introHeader}>How It Works</h1>
                <p>The answers generated by this chatbot are supported by a vast and growing knowledgebase of cyber security information.</p>
                <p>Examples of use cases for the chatbot are outlined below:</p>
                <div className={styles.useCases}>
                    <span className={styles.useCase}><FaCheckCircle className={styles.checkIcon} /> Ask questions about cyber security</span>
                    <span className={styles.useCase}><FaCheckCircle className={styles.checkIcon} /> Request information on cyber security topics</span>
                    <span className={styles.useCase}><FaCheckCircle className={styles.checkIcon} /> Learn about newly published vulnerabilities or security alerts</span>
                    <span className={styles.useCase}><FaBan className={styles.banIcon} /> Request guidance on exploiting vulnerabilities</span>
                    <span className={styles.useCase}><FaBan className={styles.banIcon} /> Request information on illegal activities</span>
                </div>
                <strong>This chatbot should only be used for legitimate, legal purposes.</strong>
            </div>
            <div className={styles.introSources}>
                <h1 className={styles.introHeader}>Cyber Security Information Sources</h1>
                <p>The chatbot uses a variety of sources to generate its responses, including:</p>
                <p className={styles.disclaimer}>Note: These links will take you to external websites.</p>
                <ul role="list" className={styles.sourcesList}>
                    {sourcesAndLinks.map((source, index) => (
                        <li key={index}>
                            <a href={source.link} target="_blank" rel="noopener noreferrer">{source.source}</a>
                        </li>
                    ))}
                </ul>
                <p>These sources provide context for the chatbot&apos;s answers, however they are not all-encompassing</p>
                <p>Additional sources of information and guidance are outlined below:</p>
                <ul role="list" className={styles.sourcesList}>
                    {additionalSourcesAndLinks.map((source, index) => (
                        <li key={index}>
                            <a href={source.link} target="_blank" rel="noopener noreferrer">{source.source}</a>
                        </li>
                    ))}
                </ul>
                <p className={styles.disclaimer}>Note: The information provided by this chatbot is accurate to the best of its knowledge, though it is important to double-check and cross-reference information provided in responses.</p>
            </div>
        </div>
    );
}