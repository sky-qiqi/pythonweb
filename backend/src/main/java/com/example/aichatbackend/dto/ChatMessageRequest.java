package com.example.aichatbackend.dto;

public class ChatMessageRequest {
    private String message;

    // Default constructor (required for JSON deserialization)
    public ChatMessageRequest() {
    }

    public ChatMessageRequest(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}