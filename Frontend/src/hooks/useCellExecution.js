import { useState, useEffect, useRef, useCallback } from 'react';

const CELL_MAX_HEIGHT = 400;
export function useCellExecution(cell, onUpdateCell) {
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      const textarea = textareaRef.current;
      textarea.style.height = 'auto';
      const scrollHeight = textarea.scrollHeight;
      const minHeight = 60; 
      const maxHeight = CELL_MAX_HEIGHT;
      const newHeight = Math.max(minHeight, Math.min(scrollHeight, maxHeight));
      textarea.style.height = `${newHeight}px`;
    }
  }, [cell.content]);

  const handleContentChange = useCallback((newContent) => {
    onUpdateCell(cell.id, { content: newContent });
  }, [cell.id, onUpdateCell]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const textarea = e.target;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newContent = cell.content.substring(0, start) + '    ' + cell.content.substring(end);

      handleContentChange(newContent);

      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 4;
      }, 0);
    }

    if (e.key === 'Tab' && e.shiftKey) {
      e.preventDefault();
      const textarea = e.target;
      const beforeCursor = cell.content.substring(0, textarea.selectionStart);
      const lastLineStart = beforeCursor.lastIndexOf('\n') + 1;
      const lineStart = cell.content.substring(lastLineStart, lastLineStart + 4);

      if (lineStart.startsWith('    ') || lineStart.startsWith('\t')) {
        const newContent = cell.content.substring(0, lastLineStart) +
                          lineStart.substring(4) +
                          cell.content.substring(textarea.selectionStart);

        handleContentChange(newContent);

        setTimeout(() => {
          textarea.selectionStart = textarea.selectionEnd = textarea.selectionStart - 4;
        }, 0);
      }
    }
  }, [cell.content, handleContentChange]);

  return {
    textareaRef,
    handleContentChange,
    handleKeyDown,
  };
}