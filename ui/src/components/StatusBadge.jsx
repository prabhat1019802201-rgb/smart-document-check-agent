export default function StatusBadge({ status }) {
  const cls =
    status === "PASS"
      ? "badge pass"
      : status === "FAIL"
      ? "badge fail"
      : "badge partial";

  return <span className={`badge ${cls}`}>{status}</span>;
}
