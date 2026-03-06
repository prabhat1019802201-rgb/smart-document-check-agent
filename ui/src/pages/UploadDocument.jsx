import { useState } from "react";
import "./upload-document.css";

export default function UploadDocument({ caseId, onUpload }) {
  const [files, setFiles] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);

  function handleSubmit() {
    if (!files || files.length === 0) {
      alert("Please select document(s)");
      return;
    }

    if (!caseId) {
      alert("Please enter Case ID in the header");
      return;
    }

    setIsProcessing(true);

    if (onUpload?.onProcessingChange) {
      onUpload.onProcessingChange(true);
    }

    onUpload({
      files,
      caseId,
    });

    setFiles([]);

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
          multiple
          accept=".pdf,.png,.jpg,.jpeg"
          onChange={(e) => setFiles(e.target.files)}
        />

        {files && files.length > 0 && (
          <div className="file-name">
            {Array.from(files).map((f, i) => (
              <div key={i}>{f.name}</div>
            ))}
          </div>
        )}
      </div>

      <div className="upload-row" style={{ justifyContent: "center" }}>
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