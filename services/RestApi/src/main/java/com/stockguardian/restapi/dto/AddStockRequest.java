package com.stockguardian.restapi.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class AddStockRequest {
    @JsonProperty("telegram_chat_id")
    @NotNull(message = "Telegram chat ID is required")
    @Positive(message = "Telegram chat ID must be a positive number")
    private Long telegramChatId;

    @JsonProperty("ticker")
    @NotBlank(message = "Ticker is required")
    private String ticker;
}
