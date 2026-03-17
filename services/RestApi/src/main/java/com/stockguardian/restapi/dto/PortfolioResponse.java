package com.stockguardian.restapi.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PortfolioResponse {
    private List<StockResponse> stocks;

    @JsonProperty("total_stocks")
    private int totalStocks;
}
