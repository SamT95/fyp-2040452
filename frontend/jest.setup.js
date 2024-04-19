import "@testing-library/jest-dom";
import { jest } from "@jest/globals";
import { server } from "@/mocks/node";

// Mock experimental 'useFormState' hook from react-dom
jest.mock("react-dom", () => ({
    ...jest.requireActual("react-dom"),
    useFormState: () => [{}, () => {}]
}));

// Establish API mocking before all tests.
beforeAll(() => server.listen());

// Reset any request handlers that we may add during the tests,
// so they don't affect other tests.
afterEach(() => server.resetHandlers());

// Clean up after the tests are finished.
afterAll(() => server.close());