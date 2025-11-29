import './MagicOutputs.css';

export default function AssemblyTableOutput({ labels, rows }) {
  const getCellClass = (columnIndex) => {
    const classes = [
      'magic-assembly-address',
      'magic-assembly-label',
      'magic-assembly-instruction',
      'magic-assembly-opcode',
      'magic-assembly-cycles',
      'magic-assembly-operand'
    ];
    return classes[columnIndex] || 'magic-assembly-cell';
  };

  return (
    <div className="magic-output">
      <h3>Assembly Table</h3>
      <table className="magic-assembly-table">
        <thead>
          <tr>
            {labels.map((label, index) => (
              <th key={index}>{label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, cellIndex) => (
                <td key={cellIndex} className={getCellClass(cellIndex)}>
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
