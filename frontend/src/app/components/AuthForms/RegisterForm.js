"use client"

import styles from "./Forms.module.css";
import { FaRegEnvelope, FaUser, FaPhoneAlt, FaLock } from "react-icons/fa";
import { Register, Verify} from "@/app/actions/register";
import Button from "@/app/components/Button/Button";
import { useFormState } from "react-dom";


const initialRegisterState = {
    success: false,
    message: '',
}

const initialVerifyState = {
    success: false,
    message: '',
}

export function RegisterForm({ onSuccess }) {
    const [state, formAction] = useFormState(Register, initialRegisterState)

    if (state.success) {
        onSuccess();
    }

    return (
        <form className={styles.authForm} action={formAction}>
            <div className={styles.formContent}>
                <div className={styles.formSection}>
                    <FaRegEnvelope />
                    <input aria-label="Email" type="email" id="email" name="email" placeholder="Email" required />
                </div>
                <div className={styles.formSection}>
                    <FaUser />
                    <input aria-label="Username" type="text" id="username" name="username" placeholder="Username" required />
                </div>
                <div className={styles.formSection}>
                    <FaLock />
                    <input aria-label="Password" type="password" id="password" name="password" placeholder="Password" required />
                </div>
            </div>
            <div className={styles.formButtons}>
                <Button type="submit" variant="primary" form>Register account</Button>
            </div>
            <p aria-label="Form status" className={state.success ? styles.formSuccess : styles.formError} aria-live="polite">
                {state.message}
            </p>
        </form>
    )
}

export function VerificationForm() {

    const [state, formAction] = useFormState(Verify, initialVerifyState);

    return (
        <form className={styles.authForm} action={formAction}>
            <div className={styles.formContent}>
                <p className={styles.verify}>
                    Please enter the verification code sent to your email.
                </p>
                <div className={styles.formSection}>
                    <FaUser />
                    <input aria-label="Username" type="text" id="username" name="username" placeholder="Username" required />
                </div>
                <div className={styles.formSection}>
                    <FaLock />
                    <input aria-label="Verification Code" type="text" id="code" name="code" placeholder="Verification code" required />
                </div>
            </div>
            <div className={styles.formButtons}>
                <Button aria-label="Submit" type="submit" variant="primary" form>Verify</Button>
            </div>
            <p aria-label="Form status" className={state.success ? styles.formSuccess : styles.formError} aria-live="polite">
                {state.message}
            </p>
        </form>
    )
}