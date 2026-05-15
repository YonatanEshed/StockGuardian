package com.stockguardian.restapi.exceptions;

import org.springframework.http.HttpStatus;

public class UserNotFoundException extends AppException {
    public UserNotFoundException(long telegramChatId) {
        super(
                "User with Telegram Chat ID " + telegramChatId + " not found.",
                ErrorCode.USER_NOT_FOUND,
                HttpStatus.NOT_FOUND
        );
    }
}
