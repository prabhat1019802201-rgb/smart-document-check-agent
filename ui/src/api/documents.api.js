import axios from "./axios";

export async function uploadDocument({ file, documentType, caseId }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("document_type", documentType);
  formData.append("case_id", caseId);

  const res = await axios.post("/documents/upload", formData);
  return res.data;
}
