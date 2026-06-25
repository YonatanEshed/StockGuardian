package com.stockguardian.restapi.services;

import com.stockguardian.restapi.dto.TickerAnalyzerStreamMessage;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
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
    private final String streamKey;

    public TickerAnalyzerPublisher(
            StringRedisTemplate redisTemplate,
            ObjectMapper objectMapper,
            @Value("${app.data.redis.ticker-analyzer-stream-key}") String streamKey) {
        this.redisTemplate = redisTemplate;
        this.objectMapper = objectMapper;
        this.streamKey = streamKey;
    }

    public String publish(String ticker) {
        String jsonPayload = objectMapper.writeValueAsString(new TickerAnalyzerStreamMessage(ticker));

        log.info("Publishing JSON payload to stream [{}]: {}", streamKey, jsonPayload);

        try {
            Map<String, String> fields = Map.of("data", jsonPayload);
            MapRecord<String, String, String> record = MapRecord.create(streamKey, fields);

            RecordId recordId = redisTemplate.opsForStream().add(record);

            log.info("Successfully published. Record ID: {}", recordId.getValue());
            return recordId.getValue();

        } catch (Exception e) {
            log.error("Failed to send payload to Redis[{}]: {}", streamKey, jsonPayload);
            throw e;
        }
    }
}
