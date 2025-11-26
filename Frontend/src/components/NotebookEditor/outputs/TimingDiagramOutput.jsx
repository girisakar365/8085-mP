import './MagicOutputs.css';

export default function TimingDiagramOutput({ instruction, diagram }) {
  return (
    <div className="magic-output magic-timing-diagram">
      <h3>Timing Diagram for {instruction}</h3>
      <img 
        src={diagram} 
        alt={`Timing Diagram for ${instruction}`} 
        className="magic-timing-image" 
      />
    </div>
  );
}
