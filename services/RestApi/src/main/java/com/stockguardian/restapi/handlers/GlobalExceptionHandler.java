package com.stockguardian.restapi.handlers;

import com.stockguardian.restapi.dto.ErrorResponse;
import com.stockguardian.restapi.exceptions.AppException;
import com.stockguardian.restapi.exceptions.ErrorCode;
import com.stockguardian.restapi.utils.ErrorResponseBuilder;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.support.DefaultMessageSourceResolvable;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.dao.OptimisticLockingFailureException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.Map;
import java.util.stream.Collectors;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException ex) {
        log.warn("Validation error: {}", ex.getMessage());

        Map<String, String> errors = ex.getBindingResult().getFieldErrors().stream()
                .collect(Collectors.toMap(
                        FieldError::getField,
                        DefaultMessageSourceResolvable::getDefaultMessage,
                        (existing, replacement) -> existing
                ));

        return ErrorResponseBuilder.buildErrorResponse(
                HttpStatus.BAD_REQUEST,
                ErrorCode.VALIDATION_ERROR,
                "Validation failed for one or more fields.",
                errors
        );
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<ErrorResponse> handleDataIntegrityViolationException(DataIntegrityViolationException ex) {
        log.warn("Data integrity violation: {}", ex.getMessage());
        return ErrorResponseBuilder.buildErrorResponse(
                HttpStatus.CONFLICT,
                ErrorCode.DATA_INTEGRITY_VIOLATION,
                "Data integrity violation. The record might already exist."
        );
    }

    @ExceptionHandler(OptimisticLockingFailureException.class)
    public ResponseEntity<ErrorResponse> handleOptimisticLockingFailureException(OptimisticLockingFailureException ex) {
        log.warn("Optimistic locking failure: {}", ex.getMessage());
        return ErrorResponseBuilder.buildErrorResponse(
                HttpStatus.CONFLICT,
                ErrorCode.OPTIMISTIC_LOCKING_FAILURE,
                "The record was modified by another transaction. Please try again."
        );
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneralException(Exception ex) {
        log.error("An unexpected error occurred: {}", ex.getMessage(), ex);
        return ErrorResponseBuilder.buildErrorResponse(
                HttpStatus.INTERNAL_SERVER_ERROR,
                ErrorCode.INTERNAL_SERVER_ERROR,
                "An unexpected error occurred. Please try again later."
        );
    }

    @ExceptionHandler(AppException.class)
    public ResponseEntity<ErrorResponse> handleAppException(AppException ex) {
        log.warn("Application error: {}", ex.getMessage());
        return ErrorResponseBuilder.buildErrorResponse(
                ex.getStatus(),
                ex.getErrorCode(),
                ex.getMessage()
        );
    }
}