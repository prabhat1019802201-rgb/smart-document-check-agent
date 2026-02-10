
export default function IssueList({ issues }) {
  if (!issues || issues.length === 0) {
    return (
      <div className="no-issues">
        ✅ No issues detected. Document passed validation.
      </div>
    );
  }

  return (
    <div className="issue-list">
      {issues.map((issue) => (
        <div key={issue.issue_id} className="issue-item">
          <div className="issue-header">
            ⚠ {(issue.field_name || "Unknown Field")
              .replaceAll("_", " ")
              .toUpperCase()}
          </div>

          <div className="issue-body">
            <p>
              <strong>Why flagged?</strong><br />
              {issue.why_flagged || "Reason not provided."}
            </p>

            <p>
              <strong>Suggested Action</strong><br />
              {issue.suggested_action || "No action suggested."}
            </p>

            {issue.severity && (
              <div className="issue-severity">
                Severity: {issue.severity}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
