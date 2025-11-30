import Cell from './Cell';

const CELL_TYPES = {
  CODE: 'code',
  MARKDOWN: 'markdown',
};

const CellList = ({
  cells,
  activeCellId,
  onCellActivate,
  onCellUpdate,
  onCellExecute,
  onCellDelete,
  onAddCell,
  onOpenAIKey
}) => {
  const handleAddBelow = (index) => {
    onAddCell(CELL_TYPES.CODE, index);
  };

  const handleRunAllAbove = (cellId) => {
    const cellIndex = cells.findIndex(c => c.id === cellId);
    if (cellIndex > 0) {
      for (let i = 0; i < cellIndex; i++) {
        onCellExecute(cells[i].id);
      }
    }
  };

  return (
    <div className="cells-container" role="main" aria-label="Notebook cells">
      {cells.map((cell, index) => (
        <Cell
          key={cell.id}
          cell={cell}
          isActive={cell.id === activeCellId}
          onUpdate={onCellUpdate}
          onRun={onCellExecute}
          onDelete={onCellDelete}
          onAddBelow={() => handleAddBelow(index)}
          onRunAllAbove={() => handleRunAllAbove(cell.id)}
          onOpenAIKey={onOpenAIKey}
          onActivate={onCellActivate}
        />
      ))}
    </div>
  );
};

export default CellList;