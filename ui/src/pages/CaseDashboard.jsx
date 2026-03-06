import { useState } from "react";
import UploadDocument from "./UploadDocument";
import IssueList from "../components/IssueList";
import CaseChat from "../components/CaseChat";
import "./case-dashboard.css";
import { uploadDocument } from "../api/documents.api";

export default function CaseDashboard({ caseId }) {

  const [currentResult, setCurrentResult] = useState(null);

  async function handleUpload(payload) {
    try {
      const result = await uploadDocument(payload);
      console.log("UPLOAD RESULT:", result); // helpful for debugging
      setCurrentResult(result);
    } catch (err) {
      console.error(err);
      alert("Upload failed. Check backend logs.");
    }
  }

  return (
    <div className="case-dashboard">

      <div className="dashboard-grid">

        {/* LEFT PANEL */}
        <div className="dashboard-panel left-panel">
          <UploadDocument
            caseId={caseId}
            onUpload={handleUpload}
          />
        </div>

        {/* RIGHT PANEL */}
        <div className="dashboard-panel right-panel">
          <div className="validation-card">
            <h3>Validation Summary & Issues</h3>

            <div className="validation-scroll">

              {currentResult && (
                <>

                  {/* Case Status */}
                  {currentResult.case_status && (
                    <div className="validation-summary">
                      <strong>Case Status:</strong> {currentResult.case_status} <br />
                      <strong>Documents Processed:</strong> {currentResult.documents_processed}
                    </div>
                  )}

                  {/* Uploaded Documents */}
                  {currentResult.uploaded_documents && (
                    <div className="validation-summary">
                      <strong>Uploaded Documents:</strong>
                      <ul>
                        {currentResult.uploaded_documents.map((doc, i) => (
                          <li key={i}>✓ {doc}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Missing Documents */}
                  {currentResult.missing_documents &&
                    currentResult.missing_documents.length > 0 && (
                      <div className="validation-summary">
                        <strong>Missing Documents:</strong>
                        <ul>
                          {currentResult.missing_documents.map((doc, i) => (
                            <li key={i}>⚠ {doc}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                  {/* DOCUMENT VALIDATION RESULTS */}
                  {currentResult.results && currentResult.results.map((doc, index) => (
                    <div key={index} className="validation-summary">

                      <h4>{doc.document_type.toUpperCase()}</h4>

                      <strong>Status:</strong> {doc.validation_summary?.status || "-"} <br />
                      <strong>Issues:</strong> {doc.validation_summary?.issues_found || 0} <br />
                      <strong>Severity:</strong> {doc.validation_summary?.severity || "-"} <br />
                      <strong>OCR Confidence:</strong> {doc.validation_summary?.ocr_confidence || "-"}

                      {/* Document Issues */}
                      <IssueList issues={doc.issues || []} />

                    </div>
                  ))}

                </>
              )}

            </div>
          </div>
        </div>

      </div>

      {/* CHAT PANEL */}
      <div className="dashboard-panel bottom-panel">
        <CaseChat caseId={caseId} />
      </div>

    </div>
  );
}
