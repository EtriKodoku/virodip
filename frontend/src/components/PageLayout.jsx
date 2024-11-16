import React, { useState, useEffect } from 'react';
import Navbar from 'react-bootstrap/Navbar';
import { useIsAuthenticated } from '@azure/msal-react';
import { SignInButton } from './SignInButton';
import { SignOutButton } from './SignOutButton';

export const PageLayout = (props) => {
    const [users, setUsers] = useState([]); // Стан для збереження користувачів
    const [userActivity, setUserActivity] = useState(null); // Стан для збереження активності користувача
    const isAuthenticated = useIsAuthenticated();

    useEffect(() => {
        // Запит до API для отримання списку користувачів
        fetch('http://localhost:5000/api/list_users')
            .then((response) => response.json())
            .then((data) => {
                setUsers(data.users); // Збереження користувачів в стан
            })
            .catch((error) => {
                console.error("Error fetching users:", error);
            });
    }, []);

    const handleEmailClick = (userId) => {
        // Запит до API для отримання активності користувача
        fetch(`http://localhost:5000/api/user_activity/${userId}`)
            .then((response) => response.json())
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
                <div className="profileContent">
                    {props.children}
                </div>
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
                                    style={{ cursor: 'pointer', color: 'blue' }}
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
                                    <strong>Time:</strong> {new Date(activity.time).toLocaleString()}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </>
    );
};
