package com.stockguardian.restapi.exceptions;

import org.springframework.http.HttpStatus;

public class StockAlreadyInPortfolioException extends AppException {
    public StockAlreadyInPortfolioException(String stockTicker) {
        super(
                "Stock with symbol '" + stockTicker + "' is already in the portfolio.",
                ErrorCode.STOCK_ALREADY_IN_PORTFOLIO,
                HttpStatus.CONFLICT
        );
    }
}
