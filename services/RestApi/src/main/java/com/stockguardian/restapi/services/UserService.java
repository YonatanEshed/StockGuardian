package com.stockguardian.restapi.services;

import com.stockguardian.restapi.dto.UserCreateRequest;
import com.stockguardian.restapi.exceptions.UserAlreadyExistsException;
import com.stockguardian.restapi.exceptions.UserNotFoundException;
import com.stockguardian.restapi.models.User;
import com.stockguardian.restapi.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * Creates a new user in the database based on the provided request data.
     *
     * @param request The request object containing the necessary information to create a user.
     * @return The ID of the newly created user.
     */
    public User createUser(UserCreateRequest request) {
        if (userRepository.existsByTelegramChatId(request.getTelegramChatId())) {
            throw new UserAlreadyExistsException(request.getTelegramChatId());
        }

        return userRepository.saveAndFlush(
                new User(
                        request.getTelegramChatId(),
                        request.getUsername()
                )
        );
    }

    /**
     * Retrieves a user from the database based on their Telegram Chat ID.
     *
     * @param telegramChatId The Telegram Chat ID of the user to retrieve.
     * @return The User object corresponding to the provided Telegram Chat ID.
     * @throws RuntimeException if no user is found with the given Telegram Chat ID.
     */
    public User getUserByTelegramChatId(Long telegramChatId) {
        return userRepository.findByTelegramChatId(telegramChatId)
                .orElseThrow(() -> new UserNotFoundException(telegramChatId));
    }
}
