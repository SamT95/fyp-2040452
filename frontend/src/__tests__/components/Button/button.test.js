import Button from "@/app/components/Button/Button";
import { render, screen } from "@testing-library/react";

describe("Button", () => {
    it("should render a button", () => {
        render(<Button />);
        const button = screen.getByRole("button");
        expect(button).toBeInTheDocument();
    });

    it("should render children correctly", () => {
        render(<Button>Click Me</Button>);
        const button = screen.getByText("Click Me");
        expect(button).toBeInTheDocument();
    });

    it("applies the primary class when variant is primary", () => {
        render(<Button variant="primary">Primary Button</Button>);
        const button = screen.getByText("Primary Button");
        expect(button).toHaveClass("primary");
    });

    it("applies the secondary class when variant is secondary", () => {
        render(<Button variant="secondary">Secondary Button</Button>);
        const button = screen.getByText("Secondary Button");
        expect(button).toHaveClass("secondary");
    });

    it("applies the formButton class when form is true", () => {
        render(<Button form>Form Button</Button>);
        const button = screen.getByText("Form Button");
        expect(button).toHaveClass("formButton");
    });

    it("applies the primary class when variant is primary and form is true", () => {
        render(<Button variant="primary" form>Primary Form Button</Button>);
        const button = screen.getByText("Primary Form Button");
        expect(button).toHaveClass("primary");
    });

    it("applies the secondary class when variant is secondary and form is true", () => {
        render(<Button variant="secondary" form>Secondary Form Button</Button>);
        const button = screen.getByText("Secondary Form Button");
        expect(button).toHaveClass("secondary");
    });

    it("handles onClick events", () => {
        const handleClick = jest.fn();
        render(<Button onClick={handleClick}>Click Me</Button>);
        const button = screen.getByText("Click Me");
        button.click();
        expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it("passes other props to the button", () => {
        render(<Button data-testid="test">Click Me</Button>);
        const button = screen.getByTestId("test");
        expect(button).toBeInTheDocument();
    });
});
