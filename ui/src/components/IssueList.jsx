import StatusBadge from "./StatusBadge";
import "./issue-list.css";

export default function IssueList({ result }) {
  if (!result) {
    return (
      <div className="issue-placeholder">
        Upload a document to see validation results.
      </div>
    );
  }

  const { validation_summary, issues } = result;

  return (
    <div className="issue-list">

      {/* STATUS BANNER */}
      <div className="validation-banner">
        <StatusBadge status={validation_summary.status} />
        <div className="summary-metrics">
          <span><b>Issues:</b> {validation_summary.issues_found}</span>
          <span><b>Severity:</b> {validation_summary.severity}</span>
          <span><b>OCR:</b> {validation_summary.ocr_confidence}</span>
        </div>
      </div>

      {/* ISSUES */}
      <div className="issues-section">
        {issues.length === 0 ? (
          <div className="no-issues">
            ✅ No issues detected. Document passed validation.
          </div>
        ) : (
          issues.map((issue, idx) => (
            <div className={`issue-card ${issue.severity?.toLowerCase()}`} key={idx}>
              <div className="issue-title">
                ⚠ {issue.field_name}
              </div>

              <div className="issue-body">
                <p><b>Why flagged:</b> {issue.why_flagged}</p>
                <p><b>Suggested action:</b> {issue.suggested_action}</p>
              </div>
            </div>
          ))
        )}
      </div>

    </div>
  );
}
