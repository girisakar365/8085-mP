import './MagicOutputs.css';

export default function SuccessOutput({ message }) {
  return (
    <div className="magic-output success">
      <div className="success-content">
        {message}
      </div>
    </div>
  );
}
