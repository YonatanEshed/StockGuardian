package com.stockguardian.restapi.exceptions;

import lombok.Getter;

/**
 * Enum representing specific error codes for application exceptions.
 */
@Getter
public enum ErrorCode {
    // Users
    USER_TELEGRAM_ID_CONFLICT("TELEGRAM_ID_CONFLICT"),

    // General
    INTERNAL_SERVER_ERROR("INTERNAL_SERVER_ERROR"),
    VALIDATION_ERROR("VALIDATION_ERROR"),
    DATA_INTEGRITY_VIOLATION("DATA_INTEGRITY_VIOLATION"),
    OPTIMISTIC_LOCKING_FAILURE("OPTIMISTIC_LOCKING_FAILURE");

    private final String code;

    ErrorCode(String code) {
        this.code = code;
    }
}
