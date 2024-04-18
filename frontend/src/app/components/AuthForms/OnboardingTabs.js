"use client"
import { RegisterForm, VerificationForm } from "./RegisterForm";
import { useState } from "react";

export default function OnboardingTabs() {
    const [currentStep, setCurrentStep] = useState("register");

    const handleRegistrationSuccess = () => {
        setCurrentStep("verify");
    }

    return (
        <>
            {currentStep === "register" ? <RegisterForm onSuccess={handleRegistrationSuccess} /> : <VerificationForm />}
        </>
    )
}