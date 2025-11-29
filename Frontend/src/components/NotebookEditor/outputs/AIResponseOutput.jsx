import './MagicOutputs.css';

export default function AIResponseOutput({ response }) {
  return (
    <div className="magic-output">
      <h3>AI Response</h3>
      <div className="magic-ai-response">{response}</div>
    </div>
  );
}
