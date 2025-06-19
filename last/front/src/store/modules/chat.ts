// src/store/modules/chat.ts
import { defineStore } from 'pinia';

interface Message {
    role: 'user' | 'assistant' | 'ai';
    content: string;
    sender: 'user' | 'ai';
}

export const useChatStore = defineStore('chat', {
    state: () => ({
        messages: [] as Message[],
    }),
    actions: {
        addMessage(message: Message) {
            this.messages.push(message);
        },
        setMessages(messages: Message[]) {
            this.messages = messages;
        },
        updateLastAiMessageContent(newContent: string) {
            if (this.messages.length > 0) {
                const lastMessage = this.messages[this.messages.length - 1];
                if (lastMessage.sender === 'ai') {
                    lastMessage.content = newContent;
                }
            }
        },
        appendLastAiMessageContent(chunk: string) {
            if (this.messages.length > 0) {
                const lastMessage = this.messages[this.messages.length - 1];
                if (lastMessage.sender === 'ai') {
                    lastMessage.content += chunk;
                }
            }
        },
        // === 新增的 action ===
        clearMessages() {
            this.messages = []; // 清空消息数组
        },
        // ==================
    },
    // persist: true, // 如果需要持久化，请在这里取消注释，并确保已安装 pinia-plugin-persistedstate 并在 main.ts 中配置
});