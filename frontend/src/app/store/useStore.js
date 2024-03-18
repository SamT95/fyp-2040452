import { create } from "zustand";

const useStore = create((set) => ({
    conversations: [
        {
            id: 1,
            sender: 'bot',
            message: 'Hello! How can I help you today?'
          }
    ],
    loading: false,
    addMessage: (message) => set((state) => ({ conversations: [...state.conversations, message] })),
    setLoading: (loading) => set(() => ({ loading })),
    updateMessage: (index, updates) => set((state) => {
        const conversations = [...state.conversations];
        conversations[index] = { ...conversations[index], ...updates };
        return { conversations: conversations }
    })
}));

export default useStore;