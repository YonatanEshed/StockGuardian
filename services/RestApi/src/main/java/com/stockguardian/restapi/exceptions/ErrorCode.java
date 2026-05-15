package com.stockguardian.restapi.exceptions;

import lombok.Getter;

/**
 * Enum representing specific error codes for application exceptions.
 */
@Getter
public enum ErrorCode {
    // Users
    USER_TELEGRAM_ID_CONFLICT("TELEGRAM_ID_CONFLICT"),
    USER_NOT_FOUND("USER_NOT_FOUND"),

    // Portfolio
    STOCK_ALREADY_IN_PORTFOLIO("STOCK_ALREADY_IN_PORTFOLIO"),
    STOCK_NOT_IN_PORTFOLIO("STOCK_NOT_IN_PORTFOLIO"),

    // General
    RESOURCE_NOT_FOUND("RESOURCE_NOT_FOUND"),
    INTERNAL_SERVER_ERROR("INTERNAL_SERVER_ERROR"),
    VALIDATION_ERROR("VALIDATION_ERROR"),
    DATA_INTEGRITY_VIOLATION("DATA_INTEGRITY_VIOLATION"),
    OPTIMISTIC_LOCKING_FAILURE("OPTIMISTIC_LOCKING_FAILURE");

    private final String code;

    ErrorCode(String code) {
        this.code = code;
    }
}
