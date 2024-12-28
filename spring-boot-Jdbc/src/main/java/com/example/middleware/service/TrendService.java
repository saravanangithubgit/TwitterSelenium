package com.example.middleware.service;

import com.example.middleware.model.Trend;
import com.example.middleware.repository.TrendRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class TrendService {

    @Autowired
    private TrendRepository trendRepository;

    public Trend saveTrend(String currentTime, String publicIp, List<String> trends) {
        Trend newTrend = new Trend();
        newTrend.setCurrentTime(currentTime);
        newTrend.setPublicIp(publicIp);
        newTrend.setTrends(trends);
        newTrend.setTimestamp(LocalDateTime.now());
        return trendRepository.save(newTrend);
    }

    public List<Trend> getAllTrends() {
        return trendRepository.findAll();
    }
}
