package com.example.middleware.dto;

import java.util.List;

public class TrendDTO {
    private String currentTime;
    private String publicIp;
    private List<String> trends;

    // Getters and Setters
    public String getCurrentTime() {
        return currentTime;
    }

    public void setCurrentTime(String currentTime) {
        this.currentTime = currentTime;
    }

    public String getPublicIp() {
        return publicIp;
    }

    public void setPublicIp(String publicIp) {
        this.publicIp = publicIp;
    }

    public List<String> getTrends() {
        return trends;
    }

    public void setTrends(List<String> trends) {
        this.trends = trends;
    }
}
