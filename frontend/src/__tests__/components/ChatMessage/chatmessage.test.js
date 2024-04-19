import ChatMessage from "@/app/components/ChatMessage/ChatMessage";
import { render, screen } from "@testing-library/react";

describe("ChatMessage", () => {
    it("should render a chat message", () => {
        render(<ChatMessage message={{ sender: "bot", message: "Hello" }} />);
        const message = screen.getByText("Hello");
        expect(message).toBeInTheDocument();
    });

    it("should render a bot message", () => {
        render(<ChatMessage message={{ sender: "bot", message: "Hello" }} />);
        const message = screen.getByText("Hello");
        expect(message).toBeInTheDocument();
    });

    it("should render a user message", () => {
        render(<ChatMessage message={{ sender: "user", message: "Hello" }} />);
        const message = screen.getByText("Hello");
        expect(message).toBeInTheDocument();
    });

    it("should render sources if they exist", () => {
        render(<ChatMessage message={{ sender: "bot", message: "Hello", sources: [{ id: "source", references: "https://source.com" }] }} />);
        const message = screen.getByText("Hello");
        const source = screen.getByText("Sources:");
        expect(message).toBeInTheDocument();
        expect(source).toBeInTheDocument();
    });

    it("should not render sources if they do not exist", () => {
        render(<ChatMessage message={{ sender: "bot", message: "Hello" }} />);
        const source = screen.queryByText("Sources:");
        expect(source).not.toBeInTheDocument();
    });

    it("should render multiple sources if they exist", () => {
        render(<ChatMessage message={{ sender: "bot", message: "Hello", sources: [{ id: "source1", references: "https://source1.com" }, { id: "source2", references: "https://source2.com" }] }} />);
        const message = screen.getByText("Hello");
        const source1 = screen.getByText("source1");
        const source2 = screen.getByText("source2");
        expect(message).toBeInTheDocument();
        expect(source1).toBeInTheDocument();
        expect(source2).toBeInTheDocument();
    });

    it("should render a link for each source", () => {
        render(<ChatMessage message={{ sender: "bot", message: "Hello", sources: [{ id: "source", references: "https://source.com" }] }} />);
        const sourceLink = screen.getByRole("link");
        expect(sourceLink).toBeInTheDocument();
    });

    it("should correctly set the href if the source has a single reference", () => {
        render(<ChatMessage message={{ sender: "bot", message: "Hello", sources: [{ id: "source", references: "https://source.com" }] }} />);
        const sourceLink = screen.getByRole("link");
        expect(sourceLink).toHaveAttribute("href", "https://source.com");
    });

    it("should correctly set the href if the source references is an array", () => {
        render(<ChatMessage message={{ sender: "bot", message: "Hello", sources: [{ id: "source", references: ["https://source1.com"] }] }} />);
        const sourceLinks = screen.getAllByRole("link");
        expect(sourceLinks[0]).toHaveAttribute("href", "https://source1.com");
    });

    it("should render a bot icon for bot messages", () => {
        render(<ChatMessage message={{ sender: "bot", message: "Hello" }} />);
        const botIcon = screen.getByLabelText("Bot icon");
        expect(botIcon).toBeInTheDocument();
    });

    it("should render a user icon for user messages", () => {
        render(<ChatMessage message={{ sender: "user", message: "Hello" }} />);
        const userIcon = screen.getByLabelText("User icon");
        expect(userIcon).toBeInTheDocument();
    });
});