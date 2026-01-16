import "./header.css";
import unionLogo from "../assets/union-bank-logo.png";

export default function Header({ caseId }) {
  const today = new Date().toLocaleDateString();

  return (
    <header className="ub-header">
      <div className="ub-header-row">
        <div className="ub-header-left">
          <img src={unionLogo} alt="Union Bank of India" />
        </div>

        <div className="ub-header-center">
          Smart Document Check Agent
        </div>

        <div className="ub-header-right">
          User ▾
        </div>
      </div>

      <div className="ub-header-sub">
        <span><strong>Case ID:</strong> {caseId || "—"}</span>
        <span><strong>Date:</strong> {today}</span>
      </div>
    </header>
  );
}
