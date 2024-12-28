package com.example.middleware.repository;

import com.example.middleware.model.Trend;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TrendRepository extends MongoRepository<Trend, String> {
}
