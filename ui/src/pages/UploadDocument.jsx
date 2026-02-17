import { useState, useEffect } from "react";
import "./upload-document.css";


export default function UploadDocument({ caseId, onUpload }) {
  const [file, setFile] = useState(null);
  const [documentType, setDocumentType] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  function handleSubmit() {
    if (!file) {
      alert("Please select a document");
      return;
    }

    // Case ID is assumed to come from Header
    if (!caseId) {
      alert("Please enter Case ID in the header");
      return;
    }
    setIsProcessing(true);

    if (onUpload?.onProcessingChange) {
     onUpload.onProcessingChange(true);
    }

    onUpload({
      file,
      documentType,
      caseId,
    });

    // optional reset
    setFile(null);
    setDocumentType("");

    // Simulate completion when parent updates (fallback safety)
    // Parent can control this properly if needed.
    setTimeout(() => {
       setIsProcessing(false);
       if (onUpload?.onProcessingChange) {
       onUpload.onProcessingChange(false);
      }
     }, 10000); 

  }

  return (

   
    <div className="ub-card upload-card">
      <div className="ub-card-title">Upload Document</div>

      <div className="upload-drop-zone">
        <div className="upload-icon">📄</div>

        <div className="upload-text">
          <strong>Drag & Drop document here</strong>
          <div className="upload-subtext">or click to upload</div>
        </div>

        <input
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          onChange={(e) => setFile(e.target.files[0])}
        />

        {file && <div className="file-name">{file.name}</div>}
      </div>

      <div className="upload-row">
        <select
          value={documentType}
          onChange={(e) => setDocumentType(e.target.value)}
        >
          <option value="">Select Document Type</option>
          <option value="aadhaar">Aadhaar</option>
          <option value="pan">PAN</option>
          <option value="cibil">CIBIL</option>
          <option value="income_proof">Income Proof</option>
          <option value="loan_request_form">Loan Application</option>
        </select>

        <button onClick={handleSubmit} disabled={isProcessing}>
          Upload & Validate
        </button>
      </div>
           {isProcessing && (
             <div className="processing-overlay">
             <div className="processing-box">
             <div className="processing-spinner"></div>
             <div className="processing-text">
                 Processing document… Running OCR & validations
             </div>
             </div>
             </div>
           )}
    </div>
  );
}

