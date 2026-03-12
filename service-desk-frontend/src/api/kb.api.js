import api from "./axios";

/* ---------------- PUBLIC ---------------- */

// Visible to users + agents + chatbot
export const getPublicFAQs = async () => {
  const res = await api.get("/kb/faqs/");
  return res.data;
};

/* ---------------- ADMIN ---------------- */

export const getAllFAQsAdmin = async () => {
  const res = await api.get("/kb/faqs/");
  return res.data;
};

export const createFAQ = async (data) => {
  const res = await api.post("/kb/faqs/", data);
  return res.data;
};

export const updateFAQ = async (id, data) => {
  const res = await api.put(`/kb/faqs/${id}/`, data);
  return res.data;
};

export const deleteFAQ = async (id) => {
  await api.delete(`/kb/faqs/${id}/`);
};

export const getKBDocuments = async () => {
  const res = await api.get("/kb/documents/");
  return res.data;
};
