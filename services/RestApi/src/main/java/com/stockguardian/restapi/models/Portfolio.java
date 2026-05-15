package com.stockguardian.restapi.models;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.Instant;

@Data
@Entity
@Table(
        name = "portfolio",
        uniqueConstraints = @UniqueConstraint(columnNames = {"user_id", "stock_id"})
)
@NoArgsConstructor
@EntityListeners(AuditingEntityListener.class)
public class Portfolio {
    public Portfolio(User user, Stock stock) {
        this.user = user;
        this.stock = stock;
    }

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    @ManyToOne
    @JoinColumn(name = "stock_id")
    private Stock stock;

    @Column(name = "added_at")
    @CreatedDate
    private Instant addedAt;
}
