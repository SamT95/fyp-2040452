import Footer from "@/app/components/Footer/Footer";
import { render, screen } from "@testing-library/react";

describe("Footer", () => {
    it("should render a footer", () => {
        render(<Footer />);
        const footer = screen.getByText("Sam Thompson / UP2040452 FYP");
        expect(footer).toBeInTheDocument();
    });

    it("should render the correct text", () => {
        render(<Footer />);
        const text = screen.getByText("Sam Thompson / UP2040452 FYP");
        expect(text).toBeInTheDocument();
    });

    it("should render a link to the GitHub repo", () => {
        render(<Footer />);
        const link = screen.getByText("GitHub");
        expect(link).toBeInTheDocument();
    });
});