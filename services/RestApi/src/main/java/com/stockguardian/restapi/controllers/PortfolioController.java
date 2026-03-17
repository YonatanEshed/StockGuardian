package com.stockguardian.restapi.controllers;

import com.stockguardian.restapi.dto.AddStockRequest;
import com.stockguardian.restapi.dto.AddStockResponse;
import com.stockguardian.restapi.models.User;
import com.stockguardian.restapi.services.PortfolioService;
import com.stockguardian.restapi.services.UserService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/portfolio")
public class PortfolioController {
    private final PortfolioService portfolioService;
    private final UserService userService;

    public PortfolioController(PortfolioService portfolioService, UserService userService) {
        this.portfolioService = portfolioService;
        this.userService = userService;
    }

    @PostMapping
    public ResponseEntity<AddStockResponse> addStockToPortfolio(@Valid @RequestBody AddStockRequest request) {
        User user = userService.getUserByTelegramChatId(request.getTelegramChatId());
        portfolioService.addStockToPortfolio(user, request.getTicker());

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(new AddStockResponse(request.getTicker(), "Stock added to portfolio successfully."));
    }
}
