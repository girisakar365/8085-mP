import {
  useState,
  useRef,
  useEffect,
  useCallback,
  memo,
  forwardRef,
} from "react";
import {
  Play,
  Trash2,
  MoreVertical,
  Loader2,
  Plus,
  Sparkles,
  ChevronDown,
  ChevronRight,
} from "lucide-react";
import { useCellExecution } from "../hooks/useCellExecution";
import { useTheme } from "../../settings/stores/settingsStore";
import groqService from "../../../shared/services/groqService";
import CellOutput from "./CellOutput";
import { marked } from 'marked';
import "./Cell.css";

const Cell = forwardRef(
  (
    {
      cell,
      isActive,
      onUpdate,
      onDelete,
      onRun,
      onRunAllAbove,
      onAddBelow,
      onOpenAIKey,
      onActivate,
    },
    ref
  ) => {
    const [showMenu, setShowMenu] = useState(false);
    const [isExplaining, setIsExplaining] = useState(false);
    const [isOutputCollapsed, setIsOutputCollapsed] = useState(false);
    const [isEditMode, setIsEditMode] = useState(false);
    const menuRef = useRef(null);
    const theme = useTheme();

    const {
      textareaRef,
      handleContentChange,
      handleKeyDown: cellHandleKeyDown,
    } = useCellExecution(cell, onUpdate);

    useEffect(() => {
      const handleClickOutside = (e) => {
        if (menuRef.current && !menuRef.current.contains(e.target)) {
          setShowMenu(false);
        }
      };

      document.addEventListener("mousedown", handleClickOutside);
      return () =>
        document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const handleCellClick = (e) => {
      if (
        e.target !== e.currentTarget &&
        !e.target.closest(".textarea-container")
      ) {
        setIsEditMode(false);
        onActivate(cell.id);
      }
    };

    const handleTextareaFocus = () => {
      setIsEditMode(true);
    };

    const handleTextareaBlur = () => {
      setIsEditMode(false);
    };

    const handleKeyDown = (e) => {
      const hasOpenDialog = document.querySelector(
        ".command-palette, .shortcuts-dialog, .api-key-dialog"
      );
      if (hasOpenDialog) return;

      if (e.key === "Escape") {
        e.preventDefault();
        setIsEditMode(false);
        e.target.blur();
        return;
      }

      if ((e.ctrlKey || e.metaKey) && e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        onRun(cell.id);
        return;
      }

      cellHandleKeyDown(e);
    };

    const getExecutionLabel = () => {
      if (cell.isExecuting) return "In [*]:";
      if (cell.executionCount !== null) return `In [${cell.executionCount}]:`;
      return "In [ ]:";
    };

    const handleExplainError = async () => {
      if (!groqService.apiKey) {
        onOpenAIKey();
        return;
      }
        // Removed invalid import for useTheme
      setIsExplaining(true);
      try {
        const explanation = await groqService.explainError(
          cell.output?.errorDetails?.code || cell.content,
          {
            line: cell.output?.errorDetails?.line,
            message: cell.output?.errorDetails?.message,
            type: "Error",
          }
        );

        onUpdate(cell.id, {
          output: {
            ...cell.output,
            aiExplanation: explanation,
          },
        });
      } catch (error) {
        if (
          error.message?.includes("API key not configured") ||
          error.message?.includes("Invalid API key") ||
          error.message?.includes("invalid API key") ||
          error.message?.includes("API_KEY_INVALID")
        ) {
          onOpenAIKey();
          return;
        }

        let errorMessage = "Failed to get AI explanation.";

        if (error.message?.includes("Rate limit exceeded")) {
          errorMessage = "Rate limit exceeded. Please try again in a moment.";
        } else if (error.message?.includes("AI model not available")) {
          errorMessage =
            "AI service temporarily unavailable. Please try again later.";
        } else if (error.message?.includes("quota")) {
          errorMessage =
            "API quota exceeded. Please check your Groq API key settings.";
        } else if (
          error.message?.includes("network") ||
          error.message?.includes("fetch")
        ) {
          errorMessage =
            "Network error. Please check your internet connection and try again.";
        } else {
          errorMessage = `Failed to get AI explanation: ${error.message}`;
        }

        alert(errorMessage);
      } finally {
        setIsExplaining(false);
      }
    };

    return (
      <>
        <div
          ref={ref}
          data-cell-id={cell.id}
          className={`cell ${cell.output?.type === "error" ? "cell-error" : ""} ${isActive ? "cell-active" : ""}`}
          role="article"
          aria-label={`Code cell ${cell.executionCount || "unexecuted"}`}
          onClick={handleCellClick}
        >
          <div className="cell-content">
            <div className="cell-sidebar">
              <span
                className="execution-counter"
                aria-label={`Execution number ${cell.executionCount || "not run"}`}
              >
                {getExecutionLabel()}
              </span>
            </div>

            <div className="cell-main">
              <div className="cell-actions">
                {cell.isExecuting ? (
                  <Loader2
                    size={18}
                    className="spinner"
                    aria-label="Cell is running"
                    role="status"
                  />
                ) : (
                  <button
                    onClick={() => onRun(cell.id)}
                    className="cell-btn run-btn"
                    title="Run Cell (Shift+Enter)"
                    aria-label="Run this cell"
                  >
                    <Play size={18} aria-hidden="true" />
                  </button>
                )}

                <div className="cell-menu" ref={menuRef}>
                  <button
                    onClick={() => setShowMenu(!showMenu)}
                    className="cell-btn menu-btn"
                    title="More Actions"
                    aria-label="Open cell menu"
                    aria-expanded={showMenu}
                    aria-haspopup="true"
                  >
                    <MoreVertical size={18} aria-hidden="true" />
                  </button>

                  {showMenu && (
                    <div
                      className="cell-dropdown"
                      role="menu"
                      aria-label="Cell actions menu"
                    >
                      <button
                        onClick={() => {
                          onRunAllAbove();
                          setShowMenu(false);
                        }}
                        role="menuitem"
                      >
                        Run All Above
                      </button>
                      <button
                        onClick={() => {
                          onAddBelow();
                          setShowMenu(false);
                        }}
                        role="menuitem"
                      >
                        Add Cell Below
                      </button>
                      <button
                        onClick={() => {
                          onUpdate(cell.id, { output: null });
                          setShowMenu(false);
                        }}
                        role="menuitem"
                      >
                        Clear Output
                      </button>
                      <button
                        onClick={() => {
                          onDelete(cell.id);
                          setShowMenu(false);
                        }}
                        className="delete-btn"
                        role="menuitem"
                      >
                        <Trash2 size={16} aria-hidden="true" /> Delete Cell
                      </button>
                    </div>
                  )}
                </div>
              </div>

              <div className="code-editor-container">
                <textarea
                  ref={textareaRef}
                  value={cell.content}
                  onChange={(e) => handleContentChange(e.target.value)}
                  onKeyDown={handleKeyDown}
                  onFocus={handleTextareaFocus}
                  onBlur={handleTextareaBlur}
                  placeholder="# Enter 8085 assembly code or magic command (@help for info)..."
                  className="cell-textarea"
                  spellCheck={false}
                  autoComplete="off"
                  autoCorrect="off"
                  autoCapitalize="off"
                  data-gramm="false"
                  aria-label="Code input"
                />
              </div>

              {cell.output && (
                <div className="cell-output-wrapper">
                  <div className="output-sidebar">
                    <span
                      className="output-label"
                      aria-label={`Output ${cell.executionCount || "empty"}`}
                    >
                      Out[{cell.executionCount || " "}]:
                    </span>
                    <button
                      onClick={() => setIsOutputCollapsed(!isOutputCollapsed)}
                      className="collapse-output-btn"
                      title={
                        isOutputCollapsed ? "Expand output" : "Collapse output"
                      }
                      aria-label={
                        isOutputCollapsed ? "Expand output" : "Collapse output"
                      }
                      aria-expanded={!isOutputCollapsed}
                    >
                      {isOutputCollapsed ? (
                        <ChevronRight size={16} aria-hidden="true" />
                      ) : (
                        <ChevronDown size={16} aria-hidden="true" />
                      )}
                    </button>
                  </div>

                  <div
                    className={`cell-output-area ${isOutputCollapsed ? "collapsed" : ""}`}
                  >
                    {!isOutputCollapsed && (
                      <>
                        <CellOutput
                          output={cell.output}
                          cellContent={cell.content}
                        />

                        {cell.output.type === "error" &&
                          cell.output.errorDetails &&
                          !cell.output.aiExplanation && (
                            <div className="ai-explain-container">
                              <button
                                onClick={handleExplainError}
                                className="ai-explain-btn"
                                disabled={isExplaining}
                                aria-label="Ask AI to explain this error"
                              >
                                <Sparkles size={16} aria-hidden="true" />
                                {isExplaining
                                  ? "Asking AI..."
                                  : "Ask AI to Explain"}
                              </button>
                            </div>
                          )}

                        {cell.output.showAIKeyButton && (
                          <div className="ai-explain-container">
                            <button
                              onClick={onOpenAIKey}
                              className="ai-configure-btn"
                              aria-label="Configure AI API key"
                            >
                              Configure AI Key
                            </button>
                          </div>
                        )}

                        {cell.output.aiExplanation && (
                          <div
                            className="ai-explanation"
                            role="complementary"
                            aria-label="AI explanation"
                          >
                            <div className="ai-explanation-header">
                              <Sparkles size={16} aria-hidden="true" />
                              <strong>AI Explanation</strong>
                            </div>
                            <div
                              className="ai-explanation-content"
                              dangerouslySetInnerHTML={{ __html: marked.parse(cell.output.aiExplanation || '') }}
                            />
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="cell-divider">
          <button
            onClick={onAddBelow}
            className="add-between-btn"
            title="Add cell below"
            aria-label="Add new cell below"
          >
            <Plus size={20} aria-hidden="true" />
          </button>
        </div>
      </>
    );
  }
);

export default memo(Cell);
