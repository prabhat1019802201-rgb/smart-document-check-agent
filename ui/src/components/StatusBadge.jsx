import "../styles/union-theme.css";

export default function StatusBadge({ status }) {
  const map = {
    PASS: "status-pass",
    PARTIAL: "status-partial",
    FAIL: "status-fail"
  };

  return (
    <span className={`status-badge ${map[status] || ""}`}>
      {status}
    </span>
  );
}
