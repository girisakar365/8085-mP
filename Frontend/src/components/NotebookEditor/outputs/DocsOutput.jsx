import './MagicOutputs.css';

export default function DocsOutput({ instruction, sections }) {
  return (
    <div className="magic-output">
      <h2>{instruction}</h2>
      <p>{sections.description.trim()}</p>
      
      {sections.args.length > 0 && (
        <div className="magic-docs-section">
          <h3>Arguments</h3>
          <pre className="magic-docs-args">{sections.args.join('\n')}</pre>
        </div>
      )}
      
      {sections.raises.length > 0 && (
        <div className="magic-docs-section">
          <h3>Raises</h3>
          <ul className="magic-docs-raises">
            {sections.raises.map((error, index) => (
              <li key={index}>{error}</li>
            ))}
          </ul>
        </div>
      )}
      
      {sections.notes.length > 0 && (
        <div className="magic-docs-section">
          <h3>Notes</h3>
          <p className="magic-docs-notes">{sections.notes.join(' ')}</p>
        </div>
      )}
      
      {sections.example.length > 0 && (
        <div className="magic-docs-section">
          <h3>Example</h3>
          <pre className="magic-docs-example">{sections.example.join('\n')}</pre>
        </div>
      )}
    </div>
  );
}
