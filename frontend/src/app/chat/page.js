import ChatContainer from "@/app/components/ChatContainer/ChatContainer";
import MessageBox from "@/app/components/MessageBox/MessageBox";
import styles from "./page.module.css";

export default function ChatPage() {
    return (
        <div className={styles.pageContainer}>
            <div className={styles.conversationContainer}>
                <ChatContainer />
                <MessageBox />
            </div>
        </div>
    )
    
}