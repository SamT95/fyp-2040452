import { RegisterForm } from "@/app/components/AuthForms/RegisterForm";
import { render, screen, fireEvent } from "@testing-library/react";

describe("RegisterForm", () => {
    it("should render a username input", () => {
        render(<RegisterForm />);
        const usernameInput = screen.getByLabelText("Username");
        expect(usernameInput).toBeInTheDocument();
    });

    it("should render a password input", () => {
        render(<RegisterForm />);
        const passwordInput = screen.getByLabelText("Password");
        expect(passwordInput).toBeInTheDocument();
    });

    it("should render a submit button", () => {
        render(<RegisterForm />);
        const submitButton = screen.getByRole("button");
        expect(submitButton).toBeInTheDocument();
    });

    it("should render a form success message", () => {
        render(<RegisterForm />);
        const formSuccess = screen.getByLabelText("Form status");
        expect(formSuccess).toHaveTextContent("");
    });
});