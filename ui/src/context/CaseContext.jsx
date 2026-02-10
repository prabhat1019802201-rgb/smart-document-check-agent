import { createContext, useContext, useState } from "react";

const CaseContext = createContext(null);

export function CaseProvider({ children }) {
  const [caseId, setCaseId] = useState("");

  return (
    <CaseContext.Provider value={{ caseId, setCaseId }}>
      {children}
    </CaseContext.Provider>
  );
}

export function useCase() {
  const ctx = useContext(CaseContext);
  if (!ctx) {
    throw new Error("useCase must be used inside CaseProvider");
  }
  return ctx;
}
