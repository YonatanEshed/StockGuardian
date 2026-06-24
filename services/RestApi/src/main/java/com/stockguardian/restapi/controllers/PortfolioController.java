package com.stockguardian.restapi.controllers;

import com.stockguardian.restapi.dto.*;
import com.stockguardian.restapi.models.Stock;
import com.stockguardian.restapi.models.User;
import com.stockguardian.restapi.services.PortfolioService;
import com.stockguardian.restapi.services.TickerAnalyzerPublisher;
import com.stockguardian.restapi.services.UserService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/portfolio")
public class PortfolioController {
    private final PortfolioService portfolioService;
    private final UserService userService;
    private final TickerAnalyzerPublisher tickerAnalyzerPublisher;

    public PortfolioController(PortfolioService portfolioService, UserService userService,
                               TickerAnalyzerPublisher tickerAnalyzerPublisher) {
        this.portfolioService = portfolioService;
        this.userService = userService;
        this.tickerAnalyzerPublisher = tickerAnalyzerPublisher;
    }

    @PostMapping
    public ResponseEntity<AddStockResponse> addStockToPortfolio(@Valid @RequestBody AddStockRequest request) {
        User user = userService.getUserByTelegramChatId(request.getTelegramChatId());
        portfolioService.addStockToPortfolio(user, request.getTicker());

        tickerAnalyzerPublisher.publish(request.getTicker());

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(new AddStockResponse(request.getTicker(), "Stock added to portfolio successfully."));
    }

    @GetMapping
    public ResponseEntity<PortfolioResponse> getUserPortfolio(@Valid @RequestBody TelegramChatRequest request) {
        User user = userService.getUserByTelegramChatId(request.getTelegramChatId());
        List<Stock> stocks = portfolioService.getUserPortfolio(user);

        List<StockResponse> portfolioStocks = stocks.stream()
                .map(stock -> new StockResponse(stock.getTicker()))
                .toList();

        return ResponseEntity
                .status(HttpStatus.OK)
                .body(new PortfolioResponse(portfolioStocks, portfolioStocks.size()));
    }

    @DeleteMapping("/{ticker}")
    public ResponseEntity<DeleteStockResponse> deleteStockFromPortfolio(
            @Valid @RequestBody TelegramChatRequest request,
            @PathVariable String ticker
    ) {
        User user = userService.getUserByTelegramChatId(request.getTelegramChatId());
        portfolioService.deleteStockFromPortfolio(user, ticker);
        return ResponseEntity
                .status(HttpStatus.OK)
                .body(new DeleteStockResponse(ticker, "Stock removed from portfolio successfully."));
    }
}
