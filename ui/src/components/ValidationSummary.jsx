import StatusBadge from "./StatusBadge";
import "../styles/union-theme.css";

export default function ValidationSummary({ summary }) {
  if (!summary) return null;

  return (
    <div className="card summary-card">
      <div className="card-header">
        Validation Summary
      </div>

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
    </div>
  );
}
