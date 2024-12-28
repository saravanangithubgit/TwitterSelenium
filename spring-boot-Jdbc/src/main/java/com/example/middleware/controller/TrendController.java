package com.example.middleware.controller;

import com.example.middleware.dto.TrendDTO;
import com.example.middleware.model.Trend;
import com.example.middleware.service.TrendService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/trends")
public class TrendController {

    @Autowired
    private TrendService trendService;

    @PostMapping
    public ResponseEntity<?> saveTrend(@Valid @RequestBody TrendDTO trendDTO) {
        try {
            Trend savedTrend = trendService.saveTrend(
                trendDTO.getCurrentTime(), 
                trendDTO.getPublicIp(), 
                trendDTO.getTrends()
            );
            return ResponseEntity.ok(savedTrend);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error saving trend: " + e.getMessage());
        }
    }

    @GetMapping
    public ResponseEntity<List<Trend>> getAllTrends() {
        List<Trend> trends = trendService.getAllTrends();
        return ResponseEntity.ok(trends);
    }

    @GetMapping("/test")
    public ResponseEntity<String> testEndpoint() {
        return ResponseEntity.ok("Endpoint is working");
    }
}
