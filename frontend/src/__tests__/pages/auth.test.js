import AuthPage from "@/app/auth/page";
import { render, screen } from "@testing-library/react";

describe("AuthPage", () => {
    it("should render the AuthTabs component", () => {
        render(<AuthPage />);
        const authTabs = screen.getByRole("tablist");
        expect(authTabs).toBeInTheDocument();
    });
});