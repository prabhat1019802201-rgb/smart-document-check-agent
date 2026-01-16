import "./validation-card.css";

export default function ValidationCard({ result }) {
  if (!result) {
    return (
      <div className="validation-card empty">
        Upload a document to see validation results.
      </div>
    );
  }

  const { validation_summary, issues } = result;

  return (
    <div className="validation-card">

      {/* SUMMARY */}
      <div className="validation-summary">
        <div>
          <strong>Status:</strong>{" "}
          <span className={`status ${validation_summary.status.toLowerCase()}`}>
            {validation_summary.status}
          </span>
        </div>
        <div><strong>Issues:</strong> {validation_summary.issues_found}</div>
        <div><strong>Severity:</strong> {validation_summary.severity}</div>
        <div><strong>OCR Confidence:</strong> {validation_summary.ocr_confidence}</div>
      </div>

      {/* ISSUES */}
      <div className="issues-scroll">
        {issues.length === 0 ? (
          <p className="no-issues">No issues found. Document passed validation.</p>
        ) : (
          issues.map((issue, idx) => (
            <div className="issue-item" key={idx}>
              <h4>{issue.field_name} — {issue.issue_type}</h4>
              <p><strong>Why flagged:</strong> {issue.why_flagged}</p>
              <p><strong>Suggested action:</strong> {issue.suggested_action}</p>
            </div>
          ))
        )}
      </div>

    </div>
  );
}
