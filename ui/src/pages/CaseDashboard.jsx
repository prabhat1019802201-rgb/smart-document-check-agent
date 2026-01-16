import "./case-dashboard.css";
//import UploadDocument from "../components/UploadDocument";
import IssueList from "../components/IssueList";
import CaseChat from "../components/CaseChat";
import ValidationSummary from "../components/ValidationSummary";
import UploadDocument from "./UploadDocument";

export default function CaseDashboard() {
  return (
    <div className="dashboard-container">
      <div className="dashboard-grid">
        
        {/* CENTER LEFT */}
        <div className="panel left-panel">
          <h2 className="section-title">Upload Document</h2>
          <UploadDocument />
        </div>

        {/* CENTER RIGHT */}
        <div className="panel right-panel">
          <h2 className="section-title">Validation Summary</h2>
          <ValidationSummary />
          <IssueList />
        </div>

        {/* BOTTOM */}
        <div className="panel bottom-panel">
          <h2 className="section-title">Ask About This Case</h2>
          <CaseChat />
        </div>

      </div>
    </div>
  );
}
