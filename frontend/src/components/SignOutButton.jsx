import React from "react";
import { useMsal } from "@azure/msal-react";

export const SignOutButton = () => {
    const { instance } = useMsal();

    const handleLogout = () => {
        instance.logoutRedirect({
            postLogoutRedirectUri: "/", // URL, на який буде перенаправлено після виходу
        }).catch(e => {
            console.log(e);
        });
    };

    return (
        <button onClick={handleLogout} className="btn btn-secondary">
            Sign Out
        </button>
    );
}
