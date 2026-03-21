package com.stockguardian.restapi.services;

import com.stockguardian.restapi.exceptions.StockAlreadyInPortfolioException;
import com.stockguardian.restapi.exceptions.StockNotInPortfolioException;
import com.stockguardian.restapi.models.Portfolio;
import com.stockguardian.restapi.models.Stock;
import com.stockguardian.restapi.models.User;
import com.stockguardian.restapi.repositories.PortfolioRepository;
import com.stockguardian.restapi.repositories.StockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

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

    /**
     * Retrieves the list of stocks in the user's portfolio.
     *
     * @param user The user whose portfolio is to be retrieved.
     * @return A list of Stock objects representing the user's portfolio.
     */
    public List<Stock> getUserPortfolio(User user) {
        return portfolioRepository.findByUser(user).stream()
                .map(Portfolio::getStock)
                .collect(Collectors.toList());
    }

    /**
     * Deletes a stock from the user's portfolio.
     *
     * @param user   The user from whose portfolio the stock will be deleted.
     * @param ticker The ticker symbol of the stock to be deleted.
     */
    public void deleteStockFromPortfolio(User user, String ticker) {
        Stock stock = stockRepository.findByTicker(ticker)
                .orElseThrow(() -> new StockNotInPortfolioException(ticker));

        Portfolio portfolioEntry = portfolioRepository.findByUserAndStock(user, stock)
                .orElseThrow(() -> new StockNotInPortfolioException(ticker));

        portfolioRepository.delete(portfolioEntry);

        // check if the stock in other user portfolio, if not delete the stock from stock table
        if (!portfolioRepository.existsByStock(stock)) {
            stockRepository.delete(stock);
        }
    }
}
