import ChatContainer from "@/app/components/ChatContainer/ChatContainer";
import { render, screen, within, act } from "@testing-library/react";
import useStore from "@/app/store/useStore";

describe("ChatContainer", () => {

    // Mock the Zustand store
    const initialState = useStore.getState();

    beforeEach(() => {
        useStore.setState(initialState, true);
    });

    it("should render a chat container", () => {
        render(<ChatContainer />);
        const chatContainer = screen.getByRole("article");
        expect(chatContainer).toBeInTheDocument();
    });

    it("should render an initial bot message", () => {
        render(<ChatContainer />);
        const botMessage = screen.getByText("Hello! How can I help you today?");
        expect(botMessage).toBeInTheDocument();
    });

    it("should render all conversation messages in zustand store", () => {
        render(<ChatContainer />);
        const conversationMessages = screen.getAllByLabelText("Chat message")
        expect(conversationMessages).toHaveLength(1);
    });

    it("should render three prompt hints when there are less than 2 messages", () => {
        render(<ChatContainer />);
        const promptHints = screen.getAllByRole("button");
        expect(promptHints).toHaveLength(3);
    });

    it("should render three prompt hints when there are less than 2 messages", () => {
        render(<ChatContainer />);
        const promptList = screen.getByRole("group");
        const { getAllByRole } = within(promptList);
        const promptHints = getAllByRole("button");
        expect(promptHints).toHaveLength(3);
    });

    it("should not render prompt hints when there are 2 or more messages", () => {
        render(<ChatContainer />);
        const mockMessages = [
            { id: 1, sender: "bot", message: "Hello" },
            { id: 2, sender: "user", message: "Hi" },
            { id: 3, sender: "bot", message: "Hey" }
        ];
        act(() => useStore.setState({ conversations: mockMessages }));
        const promptHints = screen.queryByRole("group");
        expect(promptHints).not.toBeInTheDocument();
    });
});