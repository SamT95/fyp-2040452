import { create } from "zustand";

const useStore = create((set) => ({
    conversations: [
        {
            id: 1,
            sender: 'bot',
            message: 'Hello! How can I help you today?'
          }
    ],
    chatHistories: [],
    setChatHistories: (histories) => set(() => ({ chatHistories: histories })),
    userId: "",
    setUserId: (userId) => set(() => ({ userId })),
    userName: "",
    setUserName: (userName) => set(() => ({ userName })),
    conversationId: "default",
    setConversationId: (conversationId) => set(() => ({ conversationId })),
    loading: false,
    addMessage: (message) => set((state) => ({ conversations: [...state.conversations, message] })),
    setLoading: (loading) => set(() => ({ loading })),
    updateMessage: (index, updates) => set((state) => {
        const conversations = [...state.conversations];
        conversations[index] = { ...conversations[index], ...updates };
        return { conversations: conversations }
    }),
    loadNewConversation: (messages) => set(() => ({ conversations: messages }))
}));

export default useStore;