package com.stockguardian.restapi.services;

import com.stockguardian.restapi.exceptions.StockAlreadyInPortfolioException;
import com.stockguardian.restapi.models.Portfolio;
import com.stockguardian.restapi.models.Stock;
import com.stockguardian.restapi.models.User;
import com.stockguardian.restapi.repositories.PortfolioRepository;
import com.stockguardian.restapi.repositories.StockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class PortfolioService {
    private final StockRepository stockRepository;
    private final PortfolioRepository portfolioRepository;

    @Autowired
    public PortfolioService(StockRepository stockRepository, PortfolioRepository portfolioRepository) {
        this.stockRepository = stockRepository;
        this.portfolioRepository = portfolioRepository;
    }

    /**
     * Adds a stock to the user's portfolio. If the stock does not exist in the database, it will be created.
     * If the stock is already in the user's portfolio, a StockAlreadyInPortfolioException will be thrown.
     *
     * @param user        The user to whom the stock will be added.
     * @param stockTicker The ticker symbol of the stock to be added.
     */
    @Transactional
    public void addStockToPortfolio(User user, String stockTicker) {
        Stock stock = stockRepository.findByTicker(stockTicker)
                .orElseGet(() -> stockRepository.save(new Stock(stockTicker)));

        if (portfolioRepository.existsByUserAndStock(user, stock)) {
            throw new StockAlreadyInPortfolioException(stockTicker);
        }

        portfolioRepository.save(new Portfolio(user, stock));
    }
}
