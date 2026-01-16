import { useState } from "react";
import Header from "./components/Header";
import UploadDocument from "./pages/UploadDocument";
import CaseDashboard from "./pages/CaseDashboard";

export default function App() {
  const [caseId, setCaseId] = useState("");

  return (
    <>
      <Header
        caseId={caseId}
        onCaseIdChange={setCaseId}
      />

      <main className="app-container">
        {!caseId ? (
          <UploadDocument onCaseCreated={setCaseId} />
        ) : (
          <CaseDashboard caseId={caseId} />
        )}
      </main>
    </>
  );
}
