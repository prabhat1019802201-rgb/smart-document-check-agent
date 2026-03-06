import StatusBadge from "./StatusBadge";
import "../styles/union-theme.css";

export default function ValidationSummary({ summary }) {
  if (!summary) return null;

  return (
    <div className="card summary-card">
      <div className="card-header">
        Validation Summary
      </div>

      {/* Case Status */}
      {summary.case_status && (
        <div className="case-status">
          <span className="label">Case Status</span>
          <div className="value">{summary.case_status}</div>
        </div>
      )}

      {/* Original summary grid (unchanged) */}
      <div className="summary-grid">
        <div>
          <span className="label">Status</span>
          <StatusBadge status={summary.status} />
        </div>

        <div>
          <span className="label">Issues Found</span>
          <div className="value">{summary.issues_found}</div>
        </div>

        <div>
          <span className="label">Severity</span>
          <div className="value">{summary.severity}</div>
        </div>

        <div>
          <span className="label">OCR Confidence</span>
          <div className="value">{summary.ocr_confidence}</div>
        </div>
      </div>

      {/* Uploaded Documents */}
      {summary.uploaded_documents && summary.uploaded_documents.length > 0 && (
        <div className="doc-section">
          <span className="label">Uploaded Documents</span>
          <ul>
            {summary.uploaded_documents.map((doc, index) => (
              <li key={index}>✓ {doc}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Missing Documents */}
      {summary.missing_documents && summary.missing_documents.length > 0 && (
        <div className="doc-section">
          <span className="label">Missing Documents</span>
          <ul>
            {summary.missing_documents.map((doc, index) => (
              <li key={index}>⚠ {doc}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}