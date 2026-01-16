import "./header.css";
import unionLogo from "../assets/union-bank-logo.png";

export default function Header({ caseId, onCaseIdChange }) {
  const today = new Date().toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });

  return (
    <header className="union-header">
      {/* 🔹 TOP BAR */}
      <div className="header-top">
        <img
          src={unionLogo}
          alt="Union Bank of India"
          className="bank-logo"
        />

        <div className="header-title">
          Smart Document Check Agent
        </div>
      </div>

      {/* 🔹 LOWER BAR */}
      <div className="header-bottom">
        <div className="case-id-section">
          <label>Case ID:</label>
          <input
            type="text"
            placeholder="Enter Case ID"
            value={caseId}
            onChange={(e) => onCaseIdChange(e.target.value)}
          />
        </div>

        <div className="date-section">
          Date: {today}
        </div>
      </div>
    </header>
  );
}
