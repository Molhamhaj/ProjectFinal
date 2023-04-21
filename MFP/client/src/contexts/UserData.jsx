import React from "react";

const UserData = React.createContext({
  session: {
    personal: {
      id: "",
      email: "",
      username: "",
    },
    isLoggedIn: false,
    role: "",
  },
  setSession: () => {},
});

export default UserData;
