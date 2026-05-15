package com.stockguardian.restapi.repositories;

import com.stockguardian.restapi.models.Portfolio;
import com.stockguardian.restapi.models.Stock;
import com.stockguardian.restapi.models.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface PortfolioRepository extends JpaRepository<Portfolio, Long> {
    boolean existsByUserAndStock(User user, Stock stock);

    List<Portfolio> findByUser(User user);

    Optional<Portfolio> findByUserAndStock(User user, Stock stock);

    boolean existsByStock(Stock stock);
}
