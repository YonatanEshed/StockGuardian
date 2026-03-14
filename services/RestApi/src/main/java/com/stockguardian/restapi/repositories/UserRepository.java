package com.stockguardian.restapi.repositories;

import com.stockguardian.restapi.models.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    boolean existsByTelegramChatId(long telegramChatId);
}
