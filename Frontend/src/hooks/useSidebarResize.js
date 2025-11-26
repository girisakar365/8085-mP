import { useState, useEffect, useRef } from 'react';

const LAYOUT = {
  SIDEBAR: {
    DEFAULT_WIDTH: 500,
    MIN_WIDTH: 200,
    MAX_WIDTH: 900,
  },
};

export function useSidebarResize(initialWidth = LAYOUT.SIDEBAR.DEFAULT_WIDTH) {
  const [sidebarWidth, setSidebarWidth] = useState(initialWidth);
  const [isResizing, setIsResizing] = useState(false);
  const resizeStartX = useRef(0);
  const resizeStartWidth = useRef(0);

  const handleMouseDown = (e) => {
    setIsResizing(true);
    resizeStartX.current = e.clientX;
    resizeStartWidth.current = sidebarWidth;
    e.preventDefault();
  };

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!isResizing) return;

      const deltaX = resizeStartX.current - e.clientX;
      const newWidth = Math.max(
        LAYOUT.SIDEBAR.MIN_WIDTH,
        Math.min(LAYOUT.SIDEBAR.MAX_WIDTH, resizeStartWidth.current + deltaX)
      );

      setSidebarWidth(newWidth);
    };

    const handleMouseUp = () => {
      setIsResizing(false);
    };

    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isResizing]);

  return {
    sidebarWidth,
    isResizing,
    handleMouseDown,
  };
}