package com.stockguardian.restapi.services;

import com.stockguardian.restapi.dto.UserCreateRequest;
import com.stockguardian.restapi.exceptions.UserAlreadyExistsException;
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
}
