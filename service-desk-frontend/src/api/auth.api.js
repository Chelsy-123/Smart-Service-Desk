import api from "./axios";

export const loginApi = (data) =>
  api.post("/auth/login/", data);

export const getLoggedInUser = () =>
  api.get("/users/user/");

export const createAgent = async (data) => {
  const res = await api.post("/auth/agents/create/", data);
  return res.data;
};
export const fetchAgents = () => {
  return api.get("/users/agents/");
};


// USER REGISTRATION
export const registerUser = (data) => {
  return api.post("/auth/register/", data);
};
