package com.example.aichatbackend.controller;

import com.example.aichatbackend.dto.ChatMessageRequest;
import com.example.aichatbackend.dto.ChatMessageResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

// TODO: Implement Gemini Service integration
// import com.google.cloud.vertexai.VertexAI;
// import com.google.cloud.vertexai.api.GenerateContentResponse;
// import com.google.cloud.vertexai.generativeai.GenerativeModel;
// import com.google.cloud.vertexai.generativeai.ChatSession;
// import com.google.cloud.vertexai.generativeai.ResponseHandler;

import jakarta.annotation.PostConstruct;
import java.io.IOException;

@RestController
@RequestMapping("/api/chat")
@CrossOrigin(origins = "*") // Allow requests from any origin (adjust for production)
public class ChatController {

    // TODO: Inject Gemini Service
    // private ChatSession chatSession;

    @Value("${gemini.api.key}") // Inject API key from application.properties
    private String apiKey;

    @Value("${gemini.project.id}")
    private String projectId;

    @Value("${gemini.location}")
    private String location;

    @Value("${gemini.model.name}")
    private String modelName;

    @PostConstruct
    public void init() {
        // TODO: Initialize Gemini Chat Session here using the injected properties
        System.out.println("API Key: " + apiKey); // Temporary print for verification
        System.out.println("Project ID: " + projectId);
        System.out.println("Location: " + location);
        System.out.println("Model Name: " + modelName);
        // try (VertexAI vertexAi = new VertexAI(projectId, location)) {
        //     GenerativeModel model = new GenerativeModel(modelName, vertexAi);
        //     chatSession = new ChatSession(model);
        //     System.out.println("Gemini Chat Session Initialized.");
        // } catch (IOException e) {
        //     System.err.println("Error initializing Vertex AI client: " + e.getMessage());
        //     // Handle initialization error appropriately
        // }
    }

    @PostMapping
    public ResponseEntity<ChatMessageResponse> sendMessage(@RequestBody ChatMessageRequest request) {
        if (request.getMessage() == null || request.getMessage().trim().isEmpty()) {
            return ResponseEntity.badRequest().body(new ChatMessageResponse("Message cannot be empty."));
        }

        // TODO: Replace with actual Gemini API call
        // try {
        //     System.out.println("Sending message to Gemini: " + request.getMessage());
        //     GenerateContentResponse response = chatSession.sendMessage(request.getMessage());
        //     String aiReply = ResponseHandler.getText(response);
        //     System.out.println("Received reply from Gemini: " + aiReply);
        //     return ResponseEntity.ok(new ChatMessageResponse(aiReply));
        // } catch (IOException e) {
        //     System.err.println("Error sending message to Gemini: " + e.getMessage());
        //     return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new ChatMessageResponse("Error communicating with AI service."));
        // }

        // Placeholder response
        String aiReply = "Backend received: " + request.getMessage() + " (Gemini integration pending)";
        return ResponseEntity.ok(new ChatMessageResponse(aiReply));
    }
}