import { MAGIC_COMMANDS } from "../../../services/magicCommand";
import "./MagicOutputs.css";

export default function HelpOutput() {
  return (
    <div className="magic-output">
      <h3>Available Magic Commands</h3>
      <div className="magic-help-section">
        <h4>Commands</h4>
        <div className="magic-help-commands">
          <div className="magic-help-item">
            <code className="magic-help-code">{MAGIC_COMMANDS.HELP}</code>
            <span>Display this help message</span>
          </div>
          <div className="magic-help-item">
            <code className="magic-help-code">
              {MAGIC_COMMANDS.DOCS} [instruction]
            </code>
            <span>Get documentation for an instruction</span>
          </div>
          <div className="magic-help-item">
            <code className="magic-help-code">
              {MAGIC_COMMANDS.TIMING_DIAGRAM} [instruction]
            </code>
            <span>Generate timing diagram</span>
          </div>
          <div className="magic-help-item">
            <code className="magic-help-code">
              {MAGIC_COMMANDS.ASSEMBLE} [instructions]
            </code>
            <span>Get assembly table with machine code</span>
          </div>
          <div className="magic-help-item">
            <code className="magic-help-code">
              {MAGIC_COMMANDS.ASK_AI} [question]
            </code>
            <span>Ask Google AI a question</span>
          </div>
          <div className="magic-help-item">
            <code className="magic-help-code">{MAGIC_COMMANDS.RESET}</code>
            <span>Reset processor state to default</span>
          </div>
        </div>
      </div>
      <div className="magic-help-section">
        <h4>Example Usage</h4>
        <pre className="magic-help-examples">
          {`${MAGIC_COMMANDS.DOCS} MOV
          ${MAGIC_COMMANDS.TIMING_DIAGRAM} ADD
          ${MAGIC_COMMANDS.ASSEMBLE} MVI A, 05H
          ${MAGIC_COMMANDS.ASK_AI} How does the PUSH instruction work?
          ${MAGIC_COMMANDS.RESET}`}
        </pre>
      </div>
    </div>
  );
}
