import "../styles/union-theme.css";

export default function IssueList({ issues }) {
  if (!issues || issues.length === 0) {
    return (
      <div className="card success-card">
        No issues detected. Document passed validation.
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header">
        Issues & Recommendations
      </div>

      {issues.map((issue, idx) => (
        <div key={idx} className="issue-block">
          <div className="issue-title">
            ▸ {issue.field_name.replace("_", " ").toUpperCase()}
          </div>

          <div className="issue-section">
            <strong>Why flagged?</strong>
            <p>{issue.why_flagged}</p>
          </div>

          <div className="issue-section">
            <strong>Suggested Action</strong>
            <p>{issue.suggested_action}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
