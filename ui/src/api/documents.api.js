import axios from "./axios";

export async function uploadDocument({ files, caseId }) {
  const formData = new FormData();

  // Append all files
  Array.from(files).forEach((file) => {
    formData.append("files", file);
  });

  // Append case id
  formData.append("case_id", caseId);

  const res = await axios.post("/documents/upload", formData);

  return res.data;
}
