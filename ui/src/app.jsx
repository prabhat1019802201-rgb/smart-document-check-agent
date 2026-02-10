import { useState } from "react";
import Header from "./components/Header";
import CaseDashboard from "./pages/CaseDashboard";

export default function App() {
  const [caseId, setCaseId] = useState("");

  return (
    <>
      <Header
        caseId={caseId}
        onCaseIdChange={setCaseId}
      />

      <CaseDashboard caseId={caseId} />
    </>
  );
}
