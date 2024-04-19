import Hero from "@/app/components/Hero/Hero";
import { render, screen } from "@testing-library/react";

describe("Hero", () => {
    it("should render the hero title", () => {
        render(<Hero />);
        const title = screen.getByText("Cyber Security Awareness Chatbot");
        expect(title).toBeInTheDocument();
    });

    it("should render the hero description", () => {
        render(<Hero />);
        const description = screen.getByText("A retrieval-augmented generation chatbot for cyber security knowledge and awareness");
        expect(description).toBeInTheDocument();
    });

    it("should render the get started button", () => {
        render(<Hero />);
        const button = screen.getByText("Get started");
        expect(button).toBeInTheDocument();
    });

    it("should render the register button", () => {
        render(<Hero />);
        const button = screen.getByText("Register");
        expect(button).toBeInTheDocument();
    });

    it("should render the get started button as a primary button", () => {
        render(<Hero />);
        const button = screen.getByText("Get started");
        expect(button).toHaveClass("primary");
    });

    it("should render the register button as a secondary button", () => {
        render(<Hero />);
        const button = screen.getByText("Register");
        expect(button).toHaveClass("secondary");
    });

    it("should wrap the get started button in a link to /chat", () => {
        render(<Hero />);
        const button = screen.getByText("Get started");
        expect(button.closest("a")).toHaveAttribute("href", "/chat");
    });

    it("should wrap the register button in a link to /auth", () => {
        render(<Hero />);
        const button = screen.getByText("Register");
        expect(button.closest("a")).toHaveAttribute("href", "/auth");
    });
});