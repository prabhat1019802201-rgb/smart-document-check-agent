import { useState } from "react";
import { askCaseQuestion } from "../api/caseQa.api";

export default function CaseChat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    setLoading(true);
    const res = await askCaseQuestion("LN-10234", question);
    setAnswer(res.answer);
    setLoading(false);
  };

  return (
    <div className="ub-chat">
      <strong>Ask about this case</strong>

      <input
        placeholder="Ask a question about uploaded documents..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={ask} disabled={loading}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && <div className="ub-answer">{answer}</div>}
    </div>
  );
}
