package com.example.aichatbackend.dto;

public class ChatMessageResponse {
    private String reply;

    // Default constructor (required for JSON serialization)
    public ChatMessageResponse() {
    }

    public ChatMessageResponse(String reply) {
        this.reply = reply;
    }

    public String getReply() {
        return reply;
    }

    public void setReply(String reply) {
        this.reply = reply;
    }
}