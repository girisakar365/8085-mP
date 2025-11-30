import { useState } from "react";
import { Sparkles } from "lucide-react";
import groqService from "../../../shared/services/groqService";
import { useGroqApiKey } from "../../settings/stores/settingsStore";
import { AI_PROMPTS } from "../../../constants";
import "./MagicOutputs.css";
import { marked } from 'marked';

export default function AIHelpSection({ errorData, cellContent }) {
  const [aiHelp, setAiHelp] = useState(null);
  const [isLoadingAI, setIsLoadingAI] = useState(false);
  const groqApiKey = useGroqApiKey();

  const handleAskAI = async () => {
    if (!groqApiKey) {
      setAiHelp({
        type: "warning",
        message: "Please configure your Groq API key to use AI assistance.",
      });
      return;
    }

    setIsLoadingAI(true);
    groqService.initialize(groqApiKey);

    try {
      const prompt = AI_PROMPTS.ERROR_EXPLANATION
        .replace('{code}', cellContent)
        .replace('{error}', JSON.stringify(errorData, null, 2));

      const response = await groqService.askAI(prompt);
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
          <div
            className="ai-help-content"
            dangerouslySetInnerHTML={{ __html: marked.parse(aiHelp.message || '') }}
          />
        </div>
      )}
    </div>
  );
}