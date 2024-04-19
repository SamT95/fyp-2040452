import HomePage from "@/app/page";
import { render, screen } from "@testing-library/react";

describe("HomePage", () => {
    it("should render the hero section", () => {
        render(<HomePage />);
        const hero = screen.getByText("Cyber Security Awareness Chatbot");
        expect(hero).toBeInTheDocument();
    });

    it("should render the hero description", () => {
        render(<HomePage />);
        const intro = screen.getByText("A retrieval-augmented generation chatbot for cyber security knowledge and awareness");
        expect(intro).toBeInTheDocument();
    });

    it("should render the How It Works section", () => {
        render(<HomePage />);
        const howItWorks = screen.getByText("How It Works");
        expect(howItWorks).toBeInTheDocument();
    });

    it("should render the Cyber Security Information Sources section", () => {
        render(<HomePage />);
        const sources = screen.getByText("Cyber Security Information Sources");
        expect(sources).toBeInTheDocument();
    });
});