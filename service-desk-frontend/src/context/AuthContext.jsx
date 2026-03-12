import { createContext, useState, useEffect, useContext } from "react";
import api from "../api/axios";
import { setTokens, clearTokens, getAccessToken } from "../utils/token";

export const AuthContext = createContext();

// ✅ ADD THIS HOOK (THIS FIXES EVERYTHING)
export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // 🔐 LOGIN
  const login = async ({ username, password }) => {
    const res = await api.post("/auth/login/", {
      username,
      password,
    });

    setTokens(res.data.access, res.data.refresh);
    await fetchUser();
  };

  // 👤 FETCH LOGGED-IN USER
  const fetchUser = async () => {
    try {
      const res = await api.get("/users/user/");
      setUser(res.data[0]);
    } catch (err) {
      logout();
    } finally {
      setLoading(false);
    }
  };

  // 🚪 LOGOUT
  const logout = () => {
    clearTokens();
    setUser(null);
  };

  // 🔄 LOAD USER ON REFRESH
  useEffect(() => {
    if (getAccessToken()) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        loading,
      }}
    >
      {!loading && children}
    </AuthContext.Provider>
  );
};
