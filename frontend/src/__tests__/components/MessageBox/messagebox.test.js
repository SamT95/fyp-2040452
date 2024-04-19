import MessageBox from "@/app/components/MessageBox/MessageBox";
import { render, screen, fireEvent, renderHook } from "@testing-library/react";

describe("MessageBox", () => {
    it("should render a form", () => {
        render(<MessageBox />);
        const messageBox = screen.getByTitle("Message form")
        expect(messageBox).toBeInTheDocument();
    });

    it("should render a message input field", () => {
        render(<MessageBox />);
        const messageInput = screen.getByLabelText("Message input field");
        expect(messageInput).toBeInTheDocument();
    });

    it("should render a send button", () => {
        render(<MessageBox />);
        const sendButton = screen.getByRole("button");
        expect(sendButton).toBeInTheDocument();
    });

    it("should update the message state when typing", () => {
        render(<MessageBox />);
        const messageInput = screen.getByLabelText("Message input field");
        fireEvent.change(messageInput, { target: { value: "Hello" } });
        expect(messageInput).toHaveValue("Hello");
    });

    it("should clear the message input field after sending", () => {
        render(<MessageBox />);
        const messageInput = screen.getByLabelText("Message input field");
        const sendButton = screen.getByRole("button");
        fireEvent.change(messageInput, { target: { value: "Hello" } });
        fireEvent.click(sendButton);
        expect(messageInput).toHaveValue("");
    });

    // it("should call sendMessage when the send button is clicked", () => {
    //     render(<MessageBox />);
    //     const { result, waitForNextUpdate } = renderHook(() => useChat());
    //     const sendMessageMock = jest.spyOn(result.current, "sendMessage");
    //     const setLoadingMock = jest.spyOn(useStore().default, "setLoading");
    //     useStore.mockImplementation(() => ({
    //         getState: () => ({ conversations: [] }),
    //         addMessage: jest.fn(),
    //         setLoading: setLoadingMock,
    //         updateMessage: jest.fn(),
    //     }));
    //     const messageInput = screen.getByLabelText("Message input field");
    //     const sendButton = screen.getByRole("button");
    //     const mockMessage = "Hello";
    //     act(() => {
    //         fireEvent.change(messageInput, { target: { value: mockMessage } });
    //         fireEvent.click(sendButton);
    //     })
    //     expect(sendMessageMock).toHaveBeenCalledTimes(1);
    // });

    // it("should call sendMessage when the enter key is pressed", () => {
    //     render(<MessageBox />);
    //     const messageInput = screen.getByLabelText("Message input field");
    //     fireEvent.change(messageInput, { target: { value: "Hello" } });
    //     fireEvent.keyDown(messageInput, { key: "Enter", code: 13 });
    //     expect(sendMessageMock).toHaveBeenCalledTimes(1);
    // });
});