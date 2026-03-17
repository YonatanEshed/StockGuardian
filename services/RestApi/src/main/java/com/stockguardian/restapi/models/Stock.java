package com.stockguardian.restapi.models;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Entity
@Table(name = "stocks")
@NoArgsConstructor
public class Stock {
    public Stock(String ticker) {
        this.ticker = ticker;
    }

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "ticker", unique = true)
    private String ticker;
}
