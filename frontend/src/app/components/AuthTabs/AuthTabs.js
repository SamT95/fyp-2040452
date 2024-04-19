"use client"
import styles from "./AuthTabs.module.css";
import { useState } from "react";
import OnboardingTabs from "@/app/components/AuthForms/OnboardingTabs";
import SignInTab from "@/app/components/AuthForms/SignInForm";

export default function AuthTabs() {
    const [activeTab, setActiveTab] = useState("signin");

    const handleTabChange = (tab) => {
        setActiveTab(tab);
    }

    return (
        <div className={styles.pageContainer}>
            <div className={styles.formContainer}>
                <div role="tablist" className={styles.tabButtons}>
                    <button 
                    onClick={() => handleTabChange("signin")}
                    role="tab"
                    className={`${styles.tab} ${activeTab === "signin" ? styles.active : ""}`}>
                        Sign in
                    </button>
                    <button 
                    onClick={() => handleTabChange("register")}
                    role="tab"
                    className={`${styles.tab} ${activeTab === "register" ? styles.active : ""}`}>
                        Register
                    </button>
                </div>
                <div className={styles.formBox}>
                    {activeTab === "signin" ? <SignInTab /> : <OnboardingTabs />}
                </div>
            </div>
        </div>
    );
}