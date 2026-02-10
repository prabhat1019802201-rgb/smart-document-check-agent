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
    setCurrentResult(result);
  } catch (err) {
    console.error(err);
    alert("Upload failed. Check backend logs.");
  }
}

  return (
    <div className="case-dashboard">

      <div className="dashboard-grid">

        <div className="dashboard-panel left-panel">
          <UploadDocument
            caseId={caseId}
            onUpload={handleUpload}
          />
        </div>

        <div className="dashboard-panel right-panel">
          <div className="validation-card">
            <h3>Validation Summary & Issues</h3>

            <div className="validation-scroll">

              {currentResult && (
                  <>
                  <div className="validation-summary">
                  <strong>Status:</strong> {currentResult.validation_summary.status} <br />
                  <strong>Issues:</strong> {currentResult.validation_summary.issues_found} <br />
                  <strong>Severity:</strong> {currentResult.validation_summary.severity} <br />
                  <strong>OCR Confidence:</strong> {currentResult.validation_summary.ocr_confidence}
                  </div>

                  <IssueList issues={currentResult.issues} />
                   </>
              )}

            </div>
          </div>
        </div>

      </div>

      <div className="dashboard-panel bottom-panel">
        <CaseChat caseId={caseId} />
      </div>

    </div>
  );
}
