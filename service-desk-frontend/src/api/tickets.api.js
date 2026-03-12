import api from "./axios";

export const getMyTickets = async () => {
  const res = await api.get("/tickets/tickets/");
  return res.data;
};

export const getTicketDetails = async (ticketId) => {
  const res = await api.get(`/tickets/tickets/${ticketId}/`);
  return res.data;
};

export const getTicketMessages = async (ticketId) => {
  const res = await api.get(
    `/tickets/tickets/${ticketId}/messages/`
  );
  return res.data;
};
export const submitTicketFeedback = async (ticketId, rating, comment) => {
  const res = await api.post(
    `/tickets/tickets/${ticketId}/feedback/`,
    { rating, comments: comment }
  );
  return res.data;
};

// Send message to a ticket
export const sendTicketMessage = async (ticketId, message) => {
  const res = await api.post(`/tickets/tickets/${ticketId}/messages/`, {
    message,
  });
  return res.data;
};
export const createTicket = async (data) => {
  const res = await api.post("/tickets/tickets/", data);
  return res.data;
};

export const getAssignedTickets = async () => {
  const res = await api.get("/tickets/tickets/assigned/");
  return res.data;
};

// export const getAssignedTicketDetails = async (id) => {
//   const res = await api.get(`/tickets/tickets/assigned/${id}/`);
//   return res.data;
// };


export const updateTicketStatus = async (ticketId, status) => {
  const res = await api.patch(
    `/tickets/tickets/${ticketId}/status/`,
    { status }
  );
  return res.data;
};
export const getTicketFeedback = async (ticketId) => {
  const res = await api.get(
    `/tickets/tickets/${ticketId}/feedback/`
  );
  return res.data;
}