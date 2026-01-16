import StatusBadge from "./StatusBadge";
import IssueList from "./IssueList";

export default function DocumentCard({ result }) {
  if (!result) return null;

  return (
    <div className="ub-card">
      <div className="ub-card-title">
        {result.document_type.toUpperCase()}
      </div>

      <div style={{ marginBottom: 8 }}>
        <StatusBadge status={result.validation_summary.status} />
      </div>

      <div style={{ fontSize: 13 }}>
        Issues Found: {result.validation_summary.issues_found} <br />
        Severity: {result.validation_summary.severity} <br />
        OCR Confidence: {result.validation_summary.ocr_confidence}
      </div>

      <IssueList issues={result.issues} />
    </div>
  );
}
