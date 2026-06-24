package com.stockguardian.restapi.services;

import com.stockguardian.restapi.dto.TickerAnalyzerStreamMessage;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.connection.stream.MapRecord;
import org.springframework.data.redis.connection.stream.RecordId;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import tools.jackson.databind.ObjectMapper;

import java.util.Map;

@Service
@Slf4j
public class TickerAnalyzerPublisher {

    private final StringRedisTemplate redisTemplate;
    private final ObjectMapper objectMapper;
    private static final String STREAM_KEY = "analyze-ticker"; // TODO: take this from environment variable / application properties

    public TickerAnalyzerPublisher(StringRedisTemplate redisTemplate, ObjectMapper objectMapper) {
        this.redisTemplate = redisTemplate;
        this.objectMapper = objectMapper;
    }

    public String publish(String ticker) {
        String jsonPayload = objectMapper.writeValueAsString(new TickerAnalyzerStreamMessage(ticker));

        log.info("Publishing JSON payload to stream [{}]: {}", STREAM_KEY, jsonPayload);

        try {
            Map<String, String> fields = Map.of("data", jsonPayload);
            MapRecord<String, String, String> record = MapRecord.create(STREAM_KEY, fields);

            RecordId recordId = redisTemplate.opsForStream().add(record);

            log.info("Successfully published. Record ID: {}", recordId.getValue());
            return recordId.getValue();

        } catch (Exception e) {
            log.error("Failed to send payload to Redis[{}]: {}", STREAM_KEY, jsonPayload);
            throw e;
        }
    }
}
