package com.stockguardian.restapi.exceptions;

import org.springframework.http.HttpStatus;

public class UserAlreadyExistsException extends AppException {
    public UserAlreadyExistsException(long telegramChatId) {
        super(
                "A user with the Telegram Chat ID '" + telegramChatId + "' already exists.",
                ErrorCode.USER_TELEGRAM_ID_CONFLICT,
                HttpStatus.CONFLICT
        );
    }
}
