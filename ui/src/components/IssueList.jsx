export default function IssueList({ issues = [] }) {
  if (!issues.length) return null;

  return (
    <div style={{ marginTop: 14 }}>
      <strong>Issues & Recommendations</strong>

      {issues.map((i, idx) => (
        <div key={idx} className="issue">
          <div className="issue-field">
            ▸ {i.field_name}
          </div>

          <div className="issue-text">
            <strong>Why flagged:</strong> {i.why_flagged}
          </div>

          <div className="issue-text">
            <strong>Suggested Action:</strong> {i.suggested_action}
          </div>
        </div>
      ))}
    </div>
  );
}
