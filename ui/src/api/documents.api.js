import api from "./axios";

export const uploadDocument = async (formData) => {
  const response = await api.post("/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};
