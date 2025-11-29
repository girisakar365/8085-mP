import { useState, useEffect, useCallback, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import api from '../services/api';
import { handleMagicCommand } from '../services/magicCommand';
import { useGeminiApiKey } from '../stores/settingsStore';
import { useProcessorActions } from '../stores/processorStore';
import notebookDB from '../utils/notebookDB';
import { SERVICE_CONFIG } from '../constants';
import { MAGIC_COMMANDS } from '../services/magicCommand';

const CELL_TYPES = {
  CODE: 'code',
  MARKDOWN: 'markdown',
};
const NOTEBOOK_CONFIG = {
  DEFAULT_ID: 'default-notebook',
};

const NOTEBOOK_ID = NOTEBOOK_CONFIG.DEFAULT_ID;

export default function useNotebook() {
  const [cells, setCells] = useState([
    { 
      id: uuidv4(), 
      type: CELL_TYPES.CODE, 
      content: '', 
      output: null, 
      executionCount: null, 
      isExecuting: false 
    }
  ]);
  const [activeCellId, setActiveCellId] = useState(null);
  const [globalExecutionCount, setGlobalExecutionCount] = useState(0);
  
  const executionQueueRef = useRef([]);
  const isExecutingRef = useRef(false);
  const executionCountRef = useRef(0);

  const { updateState: updateProcessorState, resetState: resetProcessorState } = useProcessorActions();
  const apiKey = useGeminiApiKey();

  useEffect(() => {
    const loadNotebook = async () => {
      try {
        const saved = await notebookDB.load(NOTEBOOK_ID);
        if (saved && saved.cells && saved.cells.length > 0) {
          setCells(saved.cells);
          setGlobalExecutionCount(saved.globalExecutionCount || 0);
          executionCountRef.current = saved.globalExecutionCount || 0;
          setActiveCellId(saved.cells[0].id);
        } else {
          executionCountRef.current = 0;
          setActiveCellId(cells[0].id);
        }
      } catch (error) {
        executionCountRef.current = 0;
        setActiveCellId(cells[0].id);
      }
    };
    loadNotebook();
  }, []);

  useEffect(() => {
    const saveNotebook = async () => {
      try {
        await notebookDB.save(NOTEBOOK_ID, { 
          cells, 
          globalExecutionCount 
        });
      } catch (error) {
      }
    };
    
    const timeoutId = setTimeout(saveNotebook, SERVICE_CONFIG.NOTEBOOK.AUTOSAVE_DELAY);
    return () => clearTimeout(timeoutId);
  }, [cells, globalExecutionCount]);

  const addCell = useCallback((type = CELL_TYPES.CODE, index = -1) => {
    const newCell = {
      id: uuidv4(),
      type,
      content: '',
      output: null,
      executionCount: null,
      isExecuting: false
    };

    setCells(prev => {
      if (index === -1) {
        return [...prev, newCell];
      }
      const newCells = [...prev];
      newCells.splice(index + 1, 0, newCell);
      return newCells;
    });
    
    setActiveCellId(newCell.id);
  }, []);

  const deleteCell = useCallback((cellId) => {
    setCells(prev => {
      const filtered = prev.filter(cell => cell.id !== cellId);
      return filtered.length > 0 ? filtered : [{ 
        id: uuidv4(), 
        type: CELL_TYPES.CODE, 
        content: '', 
        output: null, 
        executionCount: null, 
        isExecuting: false 
      }];
    });
  }, []);

  const updateCell = useCallback((cellId, updates) => {
    setCells(prev => prev.map(cell => 
      cell.id === cellId ? { ...cell, ...updates } : cell
    ));
  }, []);

  const executeCell = useCallback(async (cellId) => {
    const cell = cells.find(c => c.id === cellId);
    if (!cell || !cell.content.trim()) return;

    executionQueueRef.current.push(cellId);
    
    if (isExecutingRef.current) return;

    isExecutingRef.current = true;
    
    while (executionQueueRef.current.length > 0) {
      const currentCellId = executionQueueRef.current.shift();
      const currentCell = cells.find(c => c.id === currentCellId);
      
      if (!currentCell) continue;

      setCells(prev => prev.map(c => 
        c.id === currentCellId ? { ...c, isExecuting: true, output: null } : c
      ));

      try {
        const trimmedContent = currentCell.content.trim();

        if (trimmedContent.startsWith('@')) {
          const result = await handleMagicCommand(trimmedContent, apiKey);
          
          executionCountRef.current += 1;
          const newCount = executionCountRef.current;
          setGlobalExecutionCount(newCount);

          if (trimmedContent.startsWith(MAGIC_COMMANDS.RESET)) {
            resetProcessorState();
          }

          setCells(prev => prev.map(c => 
            c.id === currentCellId 
              ? { ...c, output: result, executionCount: newCount, isExecuting: false }
              : c
          ));
        } else {
          const result = await api.execute(trimmedContent);
          
          executionCountRef.current += 1;
          const newCount = executionCountRef.current;
          setGlobalExecutionCount(newCount);

          if (result.success && result.newState) {
            updateProcessorState(result.newState);

            setCells(prev => prev.map(c => 
              c.id === currentCellId 
                ? { 
                    ...c, 
                    output: { 
                      type: 'success', 
                      data: { message: 'Code executed successfully. Check Processor State panel.' }
                    }, 
                    executionCount: newCount, 
                    isExecuting: false 
                  }
                : c
            ));
          } else if (result.success && result.state) {
            updateProcessorState(result.state);

            setCells(prev => prev.map(c => 
              c.id === currentCellId 
                ? { 
                    ...c, 
                    output: { 
                      type: 'success', 
                      data: { message: 'Code executed successfully. Check Processor State panel.' }
                    }, 
                    executionCount: newCount, 
                    isExecuting: false 
                  }
                : c
            ));
          } else if (result.success && (result.registers || result.flags || result.memory)) {
            // Handle flat response format
            updateProcessorState({
              registers: result.registers,
              flags: result.flags,
              memory: result.memory
            });

            setCells(prev => prev.map(c => 
              c.id === currentCellId 
                ? { 
                    ...c, 
                    output: { 
                      type: 'success', 
                      data: { message: 'Code executed successfully. Check Processor State panel.' }
                    }, 
                    executionCount: newCount, 
                    isExecuting: false 
                  }
                : c
            ));
          } else if (result.success === false && result.error) {
            setCells(prev => prev.map(c => 
              c.id === currentCellId 
                ? { 
                    ...c, 
                    output: { 
                      type: 'error', 
                      data: { 
                        title: 'Execution Error',
                        message: result.error.message,
                        error: result.error
                      }
                    }, 
                    executionCount: newCount, 
                    isExecuting: false 
                  }
                : c
            ));
          } else if (result.error) {
            setCells(prev => prev.map(c => 
              c.id === currentCellId 
                ? { 
                    ...c, 
                    output: { 
                      type: 'error', 
                      data: { 
                        title: 'Execution Error',
                        message: result.message,
                        error: result.details
                      }
                    }, 
                    executionCount: newCount, 
                    isExecuting: false 
                  }
                : c
            ));
        } else {
          let stateData = null;
          
          if (result.newState) {
            stateData = result.newState;
          } else if (result.state) {
            stateData = result.state;
          } else if (result.registers || result.flags || result.memory) {
            stateData = {
              registers: result.registers,
              flags: result.flags,
              memory: result.memory
            };
          } else if (result.memory) {
            stateData = {
              registers: {},
              flags: {},
              memory: result.memory
            };
          }
          
          if (stateData) {
            updateProcessorState(stateData);
            
            setCells(prev => prev.map(c => 
              c.id === currentCellId 
                ? { 
                    ...c, 
                    output: { 
                      type: 'success', 
                      data: { message: 'Code executed successfully. Check Processor State panel.' }
                    }, 
                    executionCount: newCount, 
                    isExecuting: false 
                  }
                : c
            ));
          } else {
            setCells(prev => prev.map(c => 
              c.id === currentCellId 
                ? { 
                    ...c, 
                    output: { 
                      type: 'success', 
                      data: { message: 'Code executed successfully.' }
                    }, 
                    executionCount: newCount, 
                    isExecuting: false 
                  }
                : c
            ));
          }
        }
        }
      } catch (error) {
        executionCountRef.current += 1;
        const newCount = executionCountRef.current;
        setGlobalExecutionCount(newCount);

        setCells(prev => prev.map(c => 
          c.id === currentCellId 
            ? { 
                ...c, 
                output: { 
                  type: 'error', 
                  data: { message: error.message || 'An error occurred' }
                }, 
                executionCount: newCount, 
                isExecuting: false 
              }
            : c
        ));
      }
    }

    isExecutingRef.current = false;
  }, [cells, updateProcessorState, resetProcessorState]);

  const executeAllCells = useCallback(async () => {
    const codeCells = cells.filter(c => c.type === CELL_TYPES.CODE && c.content.trim());
    for (const cell of codeCells) {
      await executeCell(cell.id);
    }
  }, [cells, executeCell]);

  const clearAllOutputs = useCallback(() => {
    setCells(prev => prev.map(cell => ({ 
      ...cell, 
      output: null
    })));
  }, []);

  const clearAll = useCallback(() => {
    setCells([{ 
      id: uuidv4(), 
      type: CELL_TYPES.CODE, 
      content: '', 
      output: null, 
      executionCount: null, 
      isExecuting: false 
    }]);
    setGlobalExecutionCount(0);
    executionCountRef.current = 0;
    setActiveCellId(null);
  }, []);

  const importCells = useCallback((importedCells) => {
    
    if (!importedCells || !Array.isArray(importedCells)) {
      throw new Error('Invalid cells data');
    }

    const validCells = importedCells.map(cell => ({
      id: uuidv4(),
      type: cell.type || CELL_TYPES.CODE,
      content: cell.content || '',
      output: null,
      executionCount: null,
      isExecuting: false
    }));

    if (validCells.length === 0) {
      throw new Error('No valid cells to import');
    }

    setCells(validCells);
    setGlobalExecutionCount(0);
    executionCountRef.current = 0;
    setActiveCellId(validCells[0].id);
    
  }, []);

  return {
    cells,
    activeCellId,
    isExecuting: isExecutingRef.current,
    addCell,
    updateCell,
    deleteCell,
    executeCell,
    executeAllCells,
    clearAllOutputs,
    clearAll,
    importCells,
    setActiveCellId,
  };
}
