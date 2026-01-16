import { useState } from "react";
import { uploadDocument } from "../api/documents.api";

export default function UploadDocument({ onResult }) {
  const [caseId, setCaseId] = useState("");
  const [docType, setDocType] = useState("");
  const [file, setFile] = useState(null);

  const submit = async () => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("case_id", caseId);
    formData.append("document_type", docType);

    const result = await uploadDocument(formData);
    onResult(result);
  };

  return (
    <div>
      <h3>Upload Document</h3>
      <input placeholder="Case ID" onChange={e => setCaseId(e.target.value)} />
      <select onChange={e => setDocType(e.target.value)}>
        <option value="">Select Document</option>
        <option value="aadhaar">Aadhaar</option>
        <option value="pan">PAN</option>
        <option value="cibil">CIBIL</option>
        <option value="income_proof">Income Proof</option>
        <option value="loan_request_form">Loan Request Form</option>
      </select>
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={submit}>Upload</button>
    </div>
  );
}
