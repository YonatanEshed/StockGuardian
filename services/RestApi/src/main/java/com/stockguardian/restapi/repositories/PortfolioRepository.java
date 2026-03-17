package com.stockguardian.restapi.repositories;

import com.stockguardian.restapi.models.Portfolio;
import com.stockguardian.restapi.models.Stock;
import com.stockguardian.restapi.models.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PortfolioRepository extends JpaRepository<Portfolio, Long> {
    boolean existsByUserAndStock(User user, Stock stock);
}
