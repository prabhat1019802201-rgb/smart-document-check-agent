import UploadDocument from "./UploadDocument";
import IssueList from "../components/IssueList";
import CaseChat from "../components/CaseChat";
import "./case-dashboard.css";

export default function CaseDashboard() {
  return (
    <div className="case-dashboard">

      {/* MAIN GRID */}
      <div className="dashboard-grid">

        {/* LEFT PANEL — Upload */}
        <div className="dashboard-panel left-panel">
          <UploadDocument />
        </div>

        {/* RIGHT PANEL — Validation + Issues */}
        <div className="dashboard-panel right-panel">
          <div className="validation-card">
            <h3>Validation Summary & Issues</h3>

            <div className="validation-scroll">
              <IssueList />
            </div>
          </div>
        </div>

      </div>

      {/* BOTTOM PANEL — Q&A */}
      <div className="dashboard-panel bottom-panel">
        <CaseChat />
      </div>

    </div>
  );
}
