package com.stockguardian.restapi.exceptions;

import org.springframework.http.HttpStatus;

public class StockNotInPortfolioException extends AppException {
    public StockNotInPortfolioException(String ticker) {
        super(
                "Stock with ticker '" + ticker + "' is not in the portfolio.",
                ErrorCode.STOCK_NOT_IN_PORTFOLIO,
                HttpStatus.NOT_FOUND
        );
    }
}
