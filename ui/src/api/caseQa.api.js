import api from "./axios";

export const askCaseQuestion = async (caseId, question) => {
  const response = await api.post(`/cases/${caseId}/ask`, {
    question,
  });
  return response.data;
};
