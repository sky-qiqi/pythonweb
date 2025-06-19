<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue';
import { useChatStore } from '/@/store'; // 确保这里是 '/@/store'
import cxkImg from '/@/assets/img/ai/cxk.jpg';
import cxk1Img from '/@/assets/img/ai/cxk1.jpg';
import { marked } from 'marked';

const chatStore = useChatStore();

const VOLCANO_ENGINE_API_URL = 'http://127.0.0.1:8000/api/chat/';

const userInput = ref('');
const selectedImage = ref<File | null>(null);
const imagePreviewUrl = ref<string | null>(null);
const messagesContainer = ref<HTMLElement | null>(null);
const imageUploadInput = ref<HTMLInputElement | null>(null); // Add template ref
const isLoading = ref(false);

const handleImageChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    const file = input.files[0];
    selectedImage.value = file;

    // Read file as Data URL (Base64)
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreviewUrl.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);

  } else {
    selectedImage.value = null;
    imagePreviewUrl.value = null;
  }
};

const removeImage = () => {
  selectedImage.value = null;
  if (imagePreviewUrl.value) {
    URL.revokeObjectURL(imagePreviewUrl.value);
    imagePreviewUrl.value = null;
  }
  // Use template ref to clear the file input
  if (imageUploadInput.value) {
    imageUploadInput.value.value = '';
  }
};

const sendMessage = async () => {
  if (!userInput.value.trim() && !selectedImage.value || isLoading.value) {
    return;
  }

  const userMessageContent: any[] = [];
  if (userInput.value.trim()) {
    userMessageContent.push({ type: 'text', text: userInput.value.trim() });
  }
  if (selectedImage.value && imagePreviewUrl.value) {
    // For simplicity, sending base64 or a publicly accessible URL is needed.
    // The provided curl example uses a public URL.
    // In a real application, you might upload the image first and get a URL.
    // For this example, let's assume imagePreviewUrl.value is a valid URL the backend can access.
    // If sending base64 is required, you'd need to read the file and convert it.
    userMessageContent.push({ type: 'image_url', image_url: { url: imagePreviewUrl.value } });
  }

  // Add user message to chat store
  chatStore.addMessage({ role: 'user', content: userInput.value.trim(), image_url: imagePreviewUrl.value, sender: 'user' });

  userInput.value = '';
  removeImage(); // Clear selected image after sending

  await nextTick();
  scrollToBottom();

  chatStore.addMessage({ role: 'assistant', content: '', sender: 'ai' });
  isLoading.value = true;

  try {
    const response = await fetch(VOLCANO_ENGINE_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: "doubao-1-5-thinking-vision-pro-250428", // Specify the model
        messages: [
          {
            role: 'user',
            content: userMessageContent
          }
        ]
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`后端API调用失败: ${response.status} ${response.statusText} - ${errorData.detail || errorData.error || '未知错误'}`);
    }

    const reader = response.body!.getReader();
    const decoder = new TextDecoder('utf-8');
    let done = false;
    let buffer = '';

    while (!done) {
      const { value, done: readerDone } = await reader.read();
      done = readerDone;
      const chunk = decoder.decode(value, { stream: !done });
      buffer += chunk;

      let lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data:')) {
          try {
            const jsonStr = line.substring(5).trim();
            if (jsonStr === '[DONE]') {
              done = true;
              break;
            }
            const eventData = JSON.parse(jsonStr);
            if (eventData && eventData.content) {
              chatStore.appendLastAiMessageContent(eventData.content);
              await nextTick();
              scrollToBottom();
            }
          } catch (parseError) {
            console.error('解析SSE数据失败:', parseError, '原始行:', line);
          }
        }
      }
    }
    if (buffer.startsWith('data:')) {
      try {
        const jsonStr = buffer.substring(5).trim();
        if (jsonStr !== '[DONE]') {
          const eventData = JSON.parse(jsonStr);
          if (eventData && eventData.content) {
            chatStore.appendLastAiMessageContent(eventData.content);
            await nextTick();
            scrollToBottom();
          }
        }
      } catch (parseError) {
        console.error('解析剩余SSE数据失败:', parseError, '原始行:', buffer);
      }
    }

  } catch (error: any) {
    console.error('调用后端API失败:', error);
    let errorMessage = `后端API调用失败: ${error.message}`;
    if (chatStore.messages.length > 0) {
      const lastMessage = chatStore.messages[chatStore.messages.length - 1];
      if (lastMessage.sender === 'ai') {
        lastMessage.content = lastMessage.content || errorMessage;
        if (!lastMessage.content.includes(errorMessage)) {
          lastMessage.content += `\n\n错误: ${errorMessage}`;
        }
      } else {
        chatStore.addMessage({ role: 'ai', content: errorMessage, sender: 'ai' });
      }
    } else {
      chatStore.addMessage({ role: 'ai', content: errorMessage, sender: 'ai' });
    }

    await nextTick();
    scrollToBottom();
  } finally {
    isLoading.value = false;
  }
};

// === 新增的清除聊天记录函数 ===
const clearChat = () => {
  chatStore.clearMessages();
  // 清除后滚动到底部（虽然此时通常为空）
  nextTick(() => {
    scrollToBottom();
  });
};
// =============================

const renderMarkdown = (text: string) => {
  return marked(text);
};

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

onMounted(() => {
  nextTick(() => {
    scrollToBottom();
  });
});
</script>

<template>
  <div class="conversation-wrapper">
    <div class="messages" ref="messagesContainer">
      <div
          v-for="(message, index) in chatStore.messages"
          :key="index"
          :class="['message', message.sender]"
      >
        <img v-if="message.sender === 'ai'" :src="cxkImg" alt="AI Avatar" class="avatar ai-avatar" :class="{ 'shake': isLoading && message.sender === 'ai' }" />
        <div class="message-content">
          <div v-if="message.content" class="message-bubble" v-html="renderMarkdown(message.content)"></div>
          <img v-if="message.image_url" :src="message.image_url" alt="User Image" class="message-image" />
        </div>
        <img v-if="message.sender === 'user'" :src="cxk1Img" alt="User Avatar" class="avatar user-avatar" :class="{ 'shake': isLoading }" />
      </div>
    </div>
    <div class="input-area">
      <input
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="输入你的消息..."
          type="text"
          :disabled="isLoading"
  />
  <input type="file" ref="imageUploadInput" accept="image/*" @change="handleImageChange" :disabled="isLoading" style="display: none;" />
  <button @click="imageUploadInput?.click()" :disabled="isLoading">选择图片</button>
  <button @click="sendMessage" :disabled="isLoading">发送</button>
  <button @click="clearChat" :disabled="isLoading" class="clear-button">清除</button>
</div>
<div v-if="imagePreviewUrl" class="image-preview-area">
  <img :src="imagePreviewUrl" alt="Image Preview" class="image-preview" />
  <button @click="removeImage" class="remove-image-button">移除图片</button>
</div>
</div>
</template>

<style scoped>
/* 样式与你之前的保持一致 */
.conversation-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 700px;
  height: 100%;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  font-family: sans-serif;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: #f8f8f8;
  margin-top: auto;
  margin-left: auto;
  margin-right: auto;
}

.messages {
  flex-grow: 1;
  padding: 15px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: relative; /* Keep relative for z-index if needed */
  z-index: 0; /* Ensure content is above background */

}

.messages::-webkit-scrollbar {
  display: none;
}
.messages {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.message {
  display: flex;
  max-width: 85%;
  align-items: flex-start;
}

.message.user {
  justify-content: flex-end;
  align-self: flex-end;
}

.message.ai {
  justify-content: flex-start;
  align-self: flex-start;
}

.message-bubble {
  padding: 12px 18px;
  border-radius: 20px;
  word-break: break-word;
  white-space: pre-wrap;
  line-height: 1.5;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.message.user .message-bubble {
  background-color: #ff69b4; /* 少女粉 */
  color: white;
  border-bottom-right-radius: 5px;
}

.message.ai .message-bubble {
  background-color: #ffe4e1; /* 浅粉色 */
  color: #333;
  border-bottom-left-radius: 5px;
}

.input-area {
  display: flex;
  padding: 15px;
  border-top: 1px solid #ffb6c1; /* 粉色边框 */
  background-color: #fff0f5; /* 浅粉色背景 */
  flex-shrink: 0; /* Prevent shrinking */
  height: 70px; /* Give it a fixed height */
}

.input-area input {
  flex-grow: 1;
  padding: 12px;
  border: 1px solid #ffb6c1; /* 粉色边框 */
  border-radius: 20px;
  margin-right: 10px;
  font-size: 1em;
  outline: none;
  transition: border-color 0.2s;
}

.input-area input:focus {
  border-color: #ff69b4; /* 少女粉 */
}

.input-area button {
  padding: 12px 25px;
  background-color: #ff69b4; /* 少女粉 */
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}

.input-area button:hover {
  background-color: #c71585; /* 深一点的粉色 */
}

.input-area button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* === 新增的清除按钮样式 === */
.clear-button {
  background-color: #ff1493; /* 深粉色 */
  margin-left: 10px; /* 与发送按钮的间距 */
}

.clear-button:hover {
  background-color: #c71585; /* 深一点的粉色 */
}

.clear-button:disabled {
  background-color: #ffb6c1; /* 浅粉色 */
}
/* ======================== */

/* === 新增的图片相关样式 === */
.image-preview-area {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  border-top: 1px solid #ffb6c1;
  background-color: #fff0f5;
  flex-shrink: 0;
}

.image-preview {
  max-width: 100px;
  max-height: 100px;
  margin-right: 10px;
  border-radius: 5px;
  object-fit: cover;
}

.remove-image-button {
  padding: 5px 10px;
  background-color: #ff1493;
  color: white;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.2s;
}

.remove-image-button:hover {
  background-color: #c71585;
}

.message-content {
  display: flex;
  flex-direction: column;
  max-width: 100%; /* Ensure content doesn't overflow */
}

.message-image {
  max-width: 100%; /* Ensure image fits within bubble */
  max-height: 200px; /* Limit image height */
  border-radius: 10px;
  margin-top: 5px; /* Space between text and image if both exist */
  object-fit: contain; /* Ensure image is fully visible */
}
/* ======================== */

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 0 10px;
  flex-shrink: 0;
}

.message.user .avatar {
  order: 2; /* User avatar on the right */
}

.message.ai .avatar {
  /* AI avatar on the left */
}
::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('/@/assets/img/ai/hallowkity.jpg');
  background-repeat: repeat;
  background-size: auto;
  background-attachment: local; /* Ensure background scrolls with content */
  opacity: 0.8; /* 设置透明度 */
  z-index: -1; /* Ensure background is behind content */
}

/* Shake animation for AI avatar */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

.ai-avatar.shake {
  animation: shake 0.5s ease-in-out infinite;
}

</style>