import StatusBadge from "./StatusBadge";
import IssueList from "./IssueList";
import "./validation-card.css";

export default function DocumentCard({ result }) {
  if (!result) return null;

  const summary = result.validation_summary;

  return (
    <div className="ub-card validation-card">
      <div className="ub-card-title">Validation Summary</div>

      {/* Summary Section */}
      <div className="validation-summary">
        <div className="summary-row">
          <StatusBadge status={summary.status} />
        </div>

        <div className="summary-metrics">
          <div>
            <span>Issues Found</span>
            <strong>{summary.issues_found}</strong>
          </div>

          <div>
            <span>Severity</span>
            <strong>{summary.severity}</strong>
          </div>

          <div>
            <span>OCR Confidence</span>
            <strong>{summary.ocr_confidence}</strong>
          </div>
        </div>
      </div>

      {/* Issues Section */}
      <div className="issues-section">
        <div className="issues-title">Issues & Recommendations</div>
        <IssueList issues={result.issues} />
      </div>
    </div>
  );
}
