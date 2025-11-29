import { useState } from "react";
import { Sparkles } from "lucide-react";
import geminiService from "../../../services/geminiService";
import { useGeminiApiKey } from "../../../stores/settingsStore";
import { AI_PROMPTS } from "../../../constants";
import "./MagicOutputs.css";

export default function AIHelpSection({ errorData, cellContent }) {
  const [aiHelp, setAiHelp] = useState(null);
  const [isLoadingAI, setIsLoadingAI] = useState(false);
  const geminiApiKey = useGeminiApiKey();

  const handleAskAI = async () => {
    if (!geminiApiKey) {
      setAiHelp({
        type: "warning",
        message: "Please configure your Google Gemini API key to use AI assistance.",
      });
      return;
    }

    setIsLoadingAI(true);
    geminiService.initialize(geminiApiKey);

    try {
      const prompt = AI_PROMPTS.ERROR_EXPLANATION
        .replace('{code}', cellContent)
        .replace('{error}', JSON.stringify(errorData, null, 2));

      const response = await geminiService.askAI(prompt);
      setAiHelp({
        type: "success",
        message: response,
      });
    } catch (error) {
      setAiHelp({
        type: "error",
        message: "Failed to get AI help: " + error.message,
      });
    } finally {
      setIsLoadingAI(false);
    }
  };

  return (
    <div className="ai-help-section">
        <button
          onClick={handleAskAI}
          className="btn btn-primary"
        disabled={isLoadingAI}
      >
        <Sparkles size={16} />
        {isLoadingAI ? "Getting AI Help..." : "Ask AI for Help"}
      </button>

      {aiHelp && (
        <div className={`ai-help-response ${aiHelp.type}`}>
          <div className="ai-help-header">AI Assistant</div>
          <div className="ai-help-content">{aiHelp.message}</div>
        </div>
      )}
    </div>
  );
}