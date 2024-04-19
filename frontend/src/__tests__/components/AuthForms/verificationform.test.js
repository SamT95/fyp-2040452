import { VerificationForm } from "@/app/components/AuthForms/RegisterForm";
import { render, screen, fireEvent } from "@testing-library/react";

describe("VerificationForm", () => {
    it("should render a verification code input", () => {
        render(<VerificationForm />);
        const verificationCodeInput = screen.getByLabelText("Verification Code");
        expect(verificationCodeInput).toBeInTheDocument();
    });

    it("should render a username input", () => {
        render(<VerificationForm />);
        const usernameInput = screen.getByLabelText("Username");
        expect(usernameInput).toBeInTheDocument();
    });

    it("should render a submit button", () => {
        render(<VerificationForm />);
        const submitButton = screen.getByRole("button");
        expect(submitButton).toBeInTheDocument();
    });

    it("should render a form success message", () => {
        render(<VerificationForm />);
        const formSuccess = screen.getByLabelText("Form status");
        expect(formSuccess).toHaveTextContent("");
    });
});