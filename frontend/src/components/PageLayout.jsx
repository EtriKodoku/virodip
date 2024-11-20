import React, { useState, useEffect } from "react";
import Navbar from "react-bootstrap/Navbar";
import { useIsAuthenticated } from "@azure/msal-react";
import { SignInButton } from "./SignInButton";
import { SignOutButton } from "./SignOutButton";
import config from "../config"; // Імпорт конфігурації

export const PageLayout = (props) => {
    const [users, setUsers] = useState([]); // Стан для збереження користувачів
    const [userActivity, setUserActivity] = useState(null); // Стан для збереження активності користувача
    const isAuthenticated = useIsAuthenticated();

    useEffect(() => {
        const token = localStorage.getItem("authToken"); // Отримуємо токен із локального сховища

        if (!token) {
            console.error("Token not found. Ensure the user is authenticated.");
            return;
        }

        // Запит до API для отримання списку користувачів
        fetch(`${config.serverAddress}/api/list_users`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`, // Передаємо токен
            },
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch users");
                }
                return response.json();
            })
            .then((data) => {
                setUsers(data.users); // Збереження користувачів в стан
            })
            .catch((error) => {
                console.error("Error fetching users:", error);
            });
    }, []);

    const handleEmailClick = (userId) => {
        const token = localStorage.getItem("authToken"); // Отримуємо токен із локального сховища

        if (!token) {
            console.error("Token not found. Ensure the user is authenticated.");
            return;
        }

        // Запит до API для отримання активності користувача
        fetch(`${config.serverAddress}/api/user_activity/${userId}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`, // Передаємо токен
            },
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch user activity");
                }
                return response.json();
            })
            .then((data) => {
                setUserActivity(data); // Збереження даних про активність
            })
            .catch((error) => {
                console.error("Error fetching user activity:", error);
            });
    };

    return (
        <>
            <Navbar bg="primary" variant="dark" className="navbarStyle">
                <a className="navbar-brand" href="/">
                    VIRODIP PROJECT
                </a>
                <div className="profileContent">{props.children}</div>
                <div className="collapse navbar-collapse justify-content-end">
                    {isAuthenticated ? <SignOutButton /> : <SignInButton />}
                </div>
            </Navbar>

            <div className="title">
                <h5>Users List</h5>
                {/* Таблиця з користувачами */}
                <table className="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Email</th>
                            <th>At Home</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map((user) => (
                            <tr key={user.id}>
                                <td>{user.id}</td>
                                <td
                                    style={{ cursor: "pointer", color: "blue" }}
                                    onClick={() => handleEmailClick(user.id)} // Обробник події
                                >
                                    {user.email}
                                </td>
                                <td>{user.at_home ? "Yes" : "No"}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {/* Відображення активності користувача */}
                {userActivity && (
                    <div>
                        <h5>Activity of {userActivity.user.email}</h5>
                        <ul>
                            {userActivity.activities.map((activity, index) => (
                                <li key={index}>
                                    <strong>Action:</strong> {activity.action}
                                    <br />
                                    <strong>Time:</strong>{" "}
                                    {new Date(activity.time).toLocaleString()}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </>
    );
};
