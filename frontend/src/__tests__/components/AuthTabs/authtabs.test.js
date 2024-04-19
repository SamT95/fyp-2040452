import AuthTabs from "@/app/components/AuthTabs/AuthTabs";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";

describe("AuthTabs", () => {
    it("should render a sign in tab", () => {
        render(<AuthTabs />);
        // there is a sign in button and sign in tab, so we need to use the tab role
        const signInTab = screen.getByRole("tab", { name: "Sign in" });
        expect(signInTab).toBeInTheDocument();
    });

    it("should render a register tab", () => {
        render(<AuthTabs />);
        const registerTab = screen.getByText("Register");
        expect(registerTab).toBeInTheDocument();
    });

    it("should apply the active class to the sign in tab", () => {
        render(<AuthTabs />);
        const signInTab = screen.getByRole("tab", { name: "Sign in" });
        expect(signInTab).toHaveClass("active");
    });

    it("should render a username input", () => {
        render(<AuthTabs />);
        const usernameInput = screen.getByLabelText("Username");
        expect(usernameInput).toBeInTheDocument();
    });

    it("should render a password input", () => {
        render(<AuthTabs />);
        const passwordInput = screen.getByLabelText("Password");
        expect(passwordInput).toBeInTheDocument();
    });

    it("should render a sign in button", () => {
        render(<AuthTabs />);
        const submitButton = screen.getByLabelText("Submit");
        expect(submitButton).toBeInTheDocument();
    });

    it("should render a forgot password link", () => {
        render(<AuthTabs />);
        const forgotPassword = screen.getByText("Forgot password?");
        expect(forgotPassword).toBeInTheDocument();
    });

    it("should render an empty form success message", () => {
        render(<AuthTabs />);
        const formSuccess = screen.getByLabelText("Form status");
        expect(formSuccess).toHaveTextContent("");
    });

    it("should display the register tab", () => {
        render(<AuthTabs />);
        const registerTab = screen.getByRole("tab", { name: "Register" });
        expect(registerTab).toBeInTheDocument();
    });

    it("should apply the active class to the register tab when clicked", async () => {
        render(<AuthTabs />);
        const registerTab = screen.getByRole("tab", { name: "Register" });
        fireEvent.click(registerTab);
        await waitFor(() => {
            expect(registerTab).toHaveClass("active");
        });
    });
});