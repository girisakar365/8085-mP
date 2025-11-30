import { Key, Eye, EyeOff, ExternalLink, Check, X } from "lucide-react";
import { useState, useEffect } from "react";
import {
  useGeminiApiKey,
  useMaskedGeminiKey,
  useSettingsActions,
} from "../stores/settingsStore";
import groqService from "../../../shared/services/groqService";
import ConfirmDialog from "../../../shared/components/dialogs/ConfirmDialog";
import { useConfirmDialog } from "../../../shared/hooks/useConfirmDialog";
import "./APIKeyManager.css";

const ANIMATION_DURATION = {
  SLOW: 300,
};

function ExistingKeyView({ maskedKey, onUpdate, onDelete }) {
  return (
    <div className="api-key-existing">
      <div className="api-key-status">
        <Check size={20} />
        <span>API key is configured</span>
      </div>
      <div className="api-key-masked">{maskedKey}</div>
      <div className="api-key-actions">
        <button onClick={onUpdate} className="btn btn-secondary">
          Update Key
        </button>
        <button onClick={onDelete} className="btn btn-danger">
          Delete Key
        </button>
      </div>
    </div>
  );
}

function KeyInputForm({
  apiKey,
  showKey,
  isLoading,
  error,
  success,
  onKeyChange,
  onToggleVisibility,
  onSave,
  onCancel,
}) {
  return (
    <>
      <p className="api-key-description">
        Enter your Google Gemini API key to enable AI features like error
        explanations and code assistance.
      </p>

      <div className="api-key-input-group">
        <label htmlFor="api-key">API Key</label>
        <div className="api-key-input-wrapper">
          <input
            id="api-key"
            type={showKey ? "text" : "password"}
            value={apiKey}
            onChange={(e) => onKeyChange(e.target.value)}
            placeholder="Enter your Google Gemini API key"
            className="api-key-input"
            disabled={isLoading}
            autoComplete="off"
          />
          <button
            onClick={onToggleVisibility}
            className="api-key-toggle"
            title={showKey ? "Hide key" : "Show key"}
            type="button"
            disabled={isLoading}
          >
            {showKey ? <EyeOff size={20} /> : <Eye size={20} />}
          </button>
        </div>
      </div>

      {error && <div className="api-key-error">{error}</div>}

      {success && (
        <div className="api-key-success">
          <Check size={20} /> API key saved successfully
        </div>
      )}

      <div className="api-key-help">
        <p>
          <strong>Don't have an API key?</strong>
        </p>
        <a
          href="https://aistudio.google.com/app/apikey"
          target="_blank"
          rel="noopener noreferrer"
          className="api-key-link"
        >
          Get a free API key from Google AI Studio
          <ExternalLink size={20} />
        </a>
        <p className="api-key-note">
          <strong>Security:</strong> Your API key is encrypted and stored
          locally in your browser. It never leaves your device except when
          making requests to Google's API.
        </p>
      </div>

      <div className="api-key-footer">
        <button
          onClick={onCancel}
          className="btn btn-secondary"
          disabled={isLoading}
        >
          Cancel
        </button>
        <button
          onClick={onSave}
          className="btn btn-primary"
          disabled={isLoading || !apiKey.trim()}
        >
          {isLoading ? "Validating..." : "Save API Key"}
        </button>
      </div>
    </>
  );
}

function APIKeyManager({ isOpen, onClose }) {
  const [inputKey, setInputKey] = useState("");
  const [showKey, setShowKey] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [showInput, setShowInput] = useState(false);

  const geminiApiKey = useGeminiApiKey();
  const maskedGeminiKey = useMaskedGeminiKey();
  const { setGeminiApiKey, clearGeminiApiKey } = useSettingsActions();

  const { dialogState, showConfirm, closeDialog } = useConfirmDialog();

  const hasExistingKey = !!geminiApiKey;

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape" && isOpen && !isLoading) {
        handleClose();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, isLoading]);

  const handleSave = async () => {
    setError("");
    setSuccess(false);
    setIsLoading(true);

    try {
      const result = await geminiService.testApiKey(inputKey);

      if (result.valid) {
        setGeminiApiKey(inputKey);
        geminiService.initialize(inputKey);

        setSuccess(true);
        setInputKey("");

        setTimeout(() => {
          setShowInput(false);
          onClose();
          setSuccess(false);
        }, ANIMATION_DURATION.SLOW);
      } else {
        setError(result.error || "Invalid API key");
      }
    } catch (err) {
      setError(err.message || "Failed to validate API key");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    const confirmed = await showConfirm({
      title: "Delete API Key",
      message:
        "Are you sure you want to delete your API key? AI features will be disabled.",
      confirmText: "Delete",
      cancelText: "Cancel",
      variant: "danger",
    });

    if (confirmed) {
      clearGeminiApiKey();
      groqService.initialize(null);
      setShowInput(false);
    }
  };

  const handleUpdate = () => {
    setInputKey("");
    setError("");
    setSuccess(false);
    setShowInput(true);
  };

  const handleClose = () => {
    if (!isLoading) {
      setShowInput(false);
      setInputKey("");
      setError("");
      setSuccess(false);
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="api-key-overlay" onClick={handleClose}>
      <div className="api-key-dialog" onClick={(e) => e.stopPropagation()}>
        <div className="dialog-header">
          <div className="dialog-icon">
            <Key size={24} />
          </div>
          <h2>Google Gemini API Key</h2>
          <button
            onClick={handleClose}
            className="dialog-close"
            aria-label="Close"
            disabled={isLoading}
          >
            <X size={20} />
          </button>
        </div>

        <div className="api-key-content">
          {hasExistingKey && !showInput ? (
            <ExistingKeyView
              maskedKey={maskedGeminiKey}
              onUpdate={handleUpdate}
              onDelete={handleDelete}
            />
          ) : (
            <KeyInputForm
              apiKey={inputKey}
              showKey={showKey}
              isLoading={isLoading}
              error={error}
              success={success}
              onKeyChange={setInputKey}
              onToggleVisibility={() => setShowKey(!showKey)}
              onSave={handleSave}
              onCancel={handleClose}
            />
          )}
        </div>
      </div>

      <ConfirmDialog
        isOpen={dialogState.isOpen}
        onClose={dialogState.onClose || closeDialog}
        onConfirm={dialogState.onConfirm || closeDialog}
        title={dialogState.title}
        message={dialogState.message}
        confirmText={dialogState.confirmText}
        cancelText={dialogState.cancelText}
        variant={dialogState.variant}
      />
    </div>
  );
}

export default APIKeyManager;
