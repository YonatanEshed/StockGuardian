package com.stockguardian.restapi.utils;

import com.stockguardian.restapi.dto.ErrorResponse;
import com.stockguardian.restapi.exceptions.ErrorCode;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

/**
 * Utility class for building standardized error responses for the REST API.
 */
public class ErrorResponseBuilder {
    /**
     * Builds a standardized error response for the REST API without additional details.
     *
     * @param status  The HTTP status code to be returned.
     * @param message A descriptive error message explaining the reason for the error.
     * @return A ResponseEntity containing the ErrorResponse object and the specified HTTP status.
     */
    public static ResponseEntity<ErrorResponse> buildErrorResponse(HttpStatus status, ErrorCode code, String message) {
        return buildErrorResponse(status, code, message, null);
    }

    /**
     * Builds a standardized error response for the REST API.
     *
     * @param status  The HTTP status code to be returned.
     * @param message A descriptive error message explaining the reason for the error.
     * @param details Optional additional details about the error (e.g., validation errors, stack trace).
     * @return A ResponseEntity containing the ErrorResponse object and the specified HTTP status.
     */
    public static ResponseEntity<ErrorResponse> buildErrorResponse(HttpStatus status, ErrorCode code, String message, Object details) {
        ErrorResponse response = ErrorResponse.builder()
                .status(status.value())
                .error(status.getReasonPhrase())
                .message(message)
                .code(code.getCode())
                .details(details)
                .build();
        return new ResponseEntity<>(response, status);
    }
}
