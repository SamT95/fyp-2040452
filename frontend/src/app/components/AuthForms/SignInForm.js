"use client"

import styles from "./Forms.module.css";
import Button from "@/app/components/Button/Button";
import { FaUser, FaLock } from "react-icons/fa";
import SignIn from "@/app/actions/signin";
import { useFormState } from "react-dom";


const initialState = {
    success: false,
    message: '',
}

export default function SignInTab() {
    const [state, formAction] = useFormState(SignIn, initialState)

    return (
        <form className={styles.authForm} action={formAction}>
            <div className={styles.formContent}>
                <div className={styles.formSection}>
                    <FaUser />
                    <input aria-label="Username" type="text" id="username" name="username" placeholder="Username" />
                </div>
                <div className={styles.formSection}>
                    <FaLock />
                    <input aria-label="Password" type="password" id="password" name="password" placeholder="Password" />
                </div>
                <span className={styles.forgotPassword}>Forgot password?</span>
            </div>
            <div className={styles.formButtons}>
                <Button aria-label="Submit" type="submit" variant="primary" form>Sign in</Button>
            </div>
            <p aria-label="Form status" className={state.success ? styles.formSuccess : styles.formError} aria-live="polite">
                {state.message}
            </p>
        </form>
    )
}