package com.stockguardian.restapi.repositories;

import com.stockguardian.restapi.models.Stock;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface StockRepository extends JpaRepository<Stock, Long> {
    Optional<Stock> findByTicker(String ticker);
}
