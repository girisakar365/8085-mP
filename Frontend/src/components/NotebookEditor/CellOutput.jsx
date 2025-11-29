import {
  HelpOutput,
  DocsOutput,
  AssemblyTableOutput,
  TimingDiagramOutput,
  AIResponseOutput,
  ErrorOutput,
  SuccessOutput,
  WarningOutput,
  AIHelpSection,
} from "./outputs";
import "./CellOutput.css";

export default function CellOutput({ output, cellContent }) {
  console.log("CellOutput render with output:", output);

  switch (output.type) {
    case "help":
      return (
        <div className="cell-output">
          <HelpOutput />
        </div>
      );

    case "docs":
      return (
        <div className="cell-output">
          <DocsOutput
            instruction={output.data.instruction}
            sections={output.data.sections}
          />
        </div>
      );

    case "assembly-table":
      return (
        <div className="cell-output">
          <AssemblyTableOutput
            labels={output.data.labels}
            rows={output.data.rows}
          />
        </div>
      );

    case "timing-diagram":
      return (
        <div className="cell-output">
          <TimingDiagramOutput
            instruction={output.data.instruction}
            diagram={output.data.diagram}
          />
        </div>
      );

    case "ai-response":
      return (
        <div className="cell-output">
          <AIResponseOutput response={output.data.response} />
        </div>
      );

    case "success":
      return (
        <div className="cell-output">
          <SuccessOutput message={output.data.message} />
        </div>
      );

    case "warning":
      return (
        <div className="cell-output">
          <WarningOutput message={output.data.message} />
        </div>
      );

    case "error":
      return (
        <div className="cell-output">
          <ErrorOutput
            title={output.data.title}
            error={output.data.error}
            message={output.data.message}
          />
          {output.data.error && (
            <AIHelpSection
              errorData={output.data.error}
              cellContent={cellContent}
            />
          )}
        </div>
      );

    default:
      return null;
  }
}
