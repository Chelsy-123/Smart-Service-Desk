import api from "./axios";

export const sendMessageToBot = async (message) => {
  const response = await api.post("/chatbot/chat/", {
    message,
  });
  return response.data;
};

export const createTicketFromChatbot = async (payload) => {
  const response = await api.post("/chatbot/create-ticket/", payload);
  return response.data;
};
