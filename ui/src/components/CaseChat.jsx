import { useState } from "react";
import { askCaseQuestion } from "../api/caseQa.api";
import "./case-chat.css";

export default function CaseChat({ caseId }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const ask = async () => {
    if (!question.trim()) return;
    const res = await askCaseQuestion(caseId, question);
    setAnswer(res.answer);
  };

  return (
    <div className="case-chat">
      <h3>Ask about this case</h3>

      <div className="chat-input">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about validation, mismatches, income…"
        />
        <button onClick={ask}>Ask</button>
      </div>

      {answer && <div className="chat-answer">{answer}</div>}
    </div>
  );
}
