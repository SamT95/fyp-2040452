import styles from "./PromptHint.module.css";

export default function PromptHint({ prompt, handleSubmit }) {
    return (
        <button type="button" onClick={() => handleSubmit(prompt)} className={styles.promptHint}>{prompt}</button>
    )
}