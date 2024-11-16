import React from "react";
import { useMsal } from "@azure/msal-react";

export const SignOutButton = () => {
    const { instance } = useMsal();

    const handleLogout = () => {
        instance.logoutPopup({
            postLogoutRedirectUri: "/",
            mainWindowRedirectUri: "/"
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
