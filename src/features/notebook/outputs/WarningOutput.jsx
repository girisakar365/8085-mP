import './MagicOutputs.css';

export default function WarningOutput({ message }) {
  return (
    <div className="magic-output warning">
      <div className="warning-content">
        {message}
      </div>
    </div>
  );
}
