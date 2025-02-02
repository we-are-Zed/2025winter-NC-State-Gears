<template>
    <v-app>
      <v-container class="chat-container" fluid>
        <!-- Chat Card with extended size -->
        <v-card class="chat-card">
          <v-card-title class="headline">
            Chat Interface
          </v-card-title>
  
          <!-- Chat Messages Area -->
          <v-card-text class="chat-messages">
            <!-- Messages rendered here -->
            <div class="message" v-for="(msg, index) in messages" :key="index">
              {{ msg }}
            </div>
          </v-card-text>
  
          <!-- Chat Input Area with darker background -->
          <v-card-actions class="chat-input-area">
            <v-textarea
              v-model="inputText"
              placeholder="Type your message..."
              outlined
              dense
              class="chat-input"
              auto-grow
              hide-details
              @keydown.enter="sendMessage"
            />
  
            <!-- File Upload Button -->
            <v-file-input
              ref="fileInput"
              v-model="file"
              label="Upload File"
              outlined
              dense
              class="file-input"
              @change="handleFileUpload"
            />
            <span v-if="file" class="file-name">{{ file.name }}</span>
  
            <!-- Send Button -->
            <v-btn
              color="primary"
              class="send-button"
              @click="sendMessage"
              :disabled="!inputText.trim() && !file"
            >
              Send
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-container>
    </v-app>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  
  const messages = ref<string[]>([]);
  const inputText = ref('');
  const file = ref<File | null>(null);
  
  // Send the message
  function sendMessage() {
    if (inputText.value.trim()) {
      messages.value.push(inputText.value);  // Add message to chat
      inputText.value = '';  // Clear input field
    }
  
    if (file.value) {
      console.log('Uploaded file:', file.value); // Handle file upload logic
      file.value = null; // Clear the file after sending
    }
  }
  
  // Handle file upload
  function handleFileUpload(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files?.length) {
      file.value = target.files[0];
    }
  }
  </script>
  
  <style scoped>
  .chat-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
  }
  
  .chat-card {
    width: 100%;
    max-width: 800px;  /* Increased card size */
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    border: 1px solid #e0e0e0;
    background-color: #ffffff;
  }
  
  .chat-card .v-card-title {
    background-color: #1976d2;
    color: #fff;
    padding: 20px;
    font-weight: bold;
    text-align: center;
  }
  
  .chat-messages {
    max-height: 400px;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .message {
    background: #f4f4f4;
    border-radius: 8px;
    padding: 10px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    word-wrap: break-word;
  }
  
  .chat-input-area {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    border-top: 1px solid #ddd;
    background-color: #333;  /* Darker background for better contrast */
  }
  
  .chat-input {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
    color: #fff;  /* White text for contrast */
    background-color: #444;  /* Darker input background */
  }
  
  .file-input {
    max-width: 150px;
  }
  
  .file-name {
    font-size: 14px;
    margin-top: 8px;
    color: #fff;  /* White file name text for visibility */
  }
  
  .send-button {
    padding: 8px 16px;
    background: #1976d2;
    color: white;
    border-radius: 4px;
    font-size: 14px;
    border: none;
    cursor: pointer;
    transition: background 0.3s ease;
  }
  
  .send-button:hover {
    background: #115293;
  }
  
  .send-button:disabled {
    background: #b0bec5;
    cursor: not-allowed;
  }
  
  .v-file-input input[type="file"] {
    display: none;
  }
  </style>