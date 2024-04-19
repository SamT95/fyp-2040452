import PromptHint from "@/app/components/PromptHint/PromptHint";
import { render, screen } from "@testing-library/react";

describe("PromptHint", () => {
    it("should render a button", () => {
        render(<PromptHint />);
        const button = screen.getByRole("button");
        expect(button).toBeInTheDocument();
    });

    it("should render prompt prop text correctly", () => {
        render(<PromptHint prompt="Click Me" />);
        const button = screen.getByText("Click Me");
        expect(button).toBeInTheDocument();
    });

    it("handles onClick events", () => {
        const handleClick = jest.fn();
        render(<PromptHint prompt="Click Me" handleSubmit={handleClick} />);
        const button = screen.getByText("Click Me");
        button.click();
        expect(handleClick).toHaveBeenCalledTimes(1);
    });
});