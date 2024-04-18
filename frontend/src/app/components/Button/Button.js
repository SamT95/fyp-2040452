import styles from "./Button.module.css";

export default function Button({ variant, form, ...props }) {
    // Return styled button with all the same props as a normal button

    const variantClass = variant === 'primary' ? styles.primary : variant === 'secondary' ? styles.secondary : '';

    const formButton = form ? styles.formButton : '';

    // Combine the base button class with the variant class
    const buttonClass = `${styles.button} ${variantClass} ${formButton}`;
    return (
        <button type="button" className={buttonClass} {...props}>
            {props.children}
        </button>
    );
}