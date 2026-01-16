import Header from "../components/Header";
import UploadDocument from "./UploadDocument";
import DocumentCard from "../components/DocumentCard";
import CaseChat from "../components/CaseChat";

export default function CaseDashboard() {
  return (
    <>
      <Header caseId="LN-10234" />

      <div className="ub-container">
        <UploadDocument />

        <DocumentCard />

        <CaseChat />
      </div>
    </>
  );
}
