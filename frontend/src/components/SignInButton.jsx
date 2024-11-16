import React from "react";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../authConfig";
import Button from "react-bootstrap/Button";

export const SignInButton = () => {
    const { instance } = useMsal();

    const handleLogin = () => {
        instance
            .loginPopup(loginRequest) // Виконуємо вхід
            .then((loginResponse) => {
                // Після успішного входу надсилаємо POST-запит
                fetch("http://localhost:5000/api/add_user", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${loginResponse.idToken}`, // Передаємо токен
                    },
                    body: JSON.stringify({
                        name: loginResponse.account.name,        // Ім'я користувача
                        email: loginResponse.account.username,   // Email користувача
                    }),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        console.log("User added:", data); // Відповідь від бекенду
                    })
                    .catch((error) => {
                        console.error("Error sending data to backend:", error);
                    });
            })
            .catch((e) => {
                console.error("Login error:", e);
            });
    };

    return (
        <Button variant="primary" onClick={handleLogin}>
            Sign In
        </Button>
    );
};
