import { act } from 'react-dom/test-utils';
import * as zustand from 'zustand';

const { create: actualCreate, createStore: actualCreateStore } = jest.requireActual("zustand");

export const storeResetFns = new Set();

const createUncurried = (stateCreator) => {
    const store = actualCreate(stateCreator);
    const initialState = store.getState();
    storeResetFns.add(() => store.setState(initialState, true));
    return store;
}

export const create = (stateCreator) => {
    console.log("zustand create mock")
    return typeof stateCreator === "function" ? createUncurried(stateCreator) : createUncurried
}

const createStoreUncurried = (stateCreator) => {
    const store = actualCreateStore(stateCreator);
    const initialState = store.getState();
    storeResetFns.add(() => store.setState(initialState, true));
    return store;
}

export const createStore = (stateCreator) => {
    return typeof stateCreator === "function" ? createStoreUncurried(stateCreator) : createStoreUncurried
}


// const create = () => (createState) => {
//     const store = actualCreate(createState);
//     const initialState = store.getState();
//     storeResetFns.add(() => store.setState(initialState, true));
//     return store;
// }

// const createMockStore = () => (createState) => {
//     const store = actualCreate(createState);
//     const initialState = store.getState();
//     storeResetFunctions.add(() => store.setState(initialState));
//     return store;
// }

beforeEach(async () => {
    await act(() => storeResetFns.forEach((resetFn) => resetFn()));
})

// export { create };