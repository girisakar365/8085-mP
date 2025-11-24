import "./MagicOutputs.css";

export default function ErrorOutput({ title = "Error", error, message }) {
  let mainMessage = "An unknown error occurred";
  if (message) {
    mainMessage = message;
  } else if (typeof error === "string") {
    mainMessage = error;
  } else if (error?.message) {
    mainMessage = error.message;
  } else if (error?.detail) {
    mainMessage = error.detail;
  }

  const detailLines = [];
  if (error && typeof error === "object") {
    if (error.instruction)
      detailLines.push(`Instruction : ${error.instruction}`);
    if (error.type) detailLines.push(`Type        : ${error.type}`);
    if (error.position !== undefined)
      detailLines.push(`Position    : ${error.position}`);
    if (error.line) detailLines.push(`Problem Line: ${error.line}`);
  }

  return (
    <div className="magic-output error">
      <h2>{title}</h2>
      <p>{mainMessage}</p>
      {detailLines.length > 0 && (
        <div className="magic-docs-section">
          <h3>Details</h3>
          <pre className="magic-error-details">{detailLines.join("\n")}</pre>
        </div>
      )}
      {error?.hint && (
        <div className="magic-docs-section">
          <h3>Hint</h3>
          <p className="magic-error-hint">{error.hint}</p>
        </div>
      )}
    </div>
  );
}
