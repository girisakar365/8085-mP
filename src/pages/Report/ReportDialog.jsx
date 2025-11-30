import React, { useState } from 'react';
import { X, Flag } from 'lucide-react';
import reportService from '../../shared/services/reportService';
import './ReportDialog.css';

export default function ReportDialog({ isOpen, onClose }) {
  const [reportText, setReportText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!reportText.trim()) return;

    setIsSubmitting(true);
    
    try {
      await reportService.submitReport(reportText);
      setSubmitted(true);
      setReportText('');
    } catch (error) {
      console.error('Failed to submit report:', error);
      // ERROR HANDLING NEEDED
      alert('Failed to send report. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    if (!isSubmitting) {
      setReportText('');
      setSubmitted(false);
      onClose();
    }
  };

  return (
    <div className="dialog-overlay" onClick={handleClose}>
      <div className="dialog" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
        <div className="dialog-header">
          <div className="dialog-icon">
            <Flag size={24} />
          </div>
          <h2>Report an Issue</h2>
          <button className="dialog-close" onClick={handleClose} aria-label="Close" disabled={isSubmitting}>
            <X size={20} />
          </button>
        </div>
        
        {submitted ? (
          <div className="dialog-success">
            <div className="success-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <circle cx="24" cy="24" r="22" stroke="currentColor" strokeWidth="2"/>
                <path d="M14 24l8 8 12-16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <h3>Report Sent Successfully</h3>
            <p>Thank you for your feedback. We'll review your report and get back to you if needed.</p>
          </div>
        ) : (
          <>
            <div className="dialog-body">
              <p className="dialog-description">
                Describe the problem you encountered. Include steps to reproduce the issue if possible.
              </p>
              
              <form onSubmit={handleSubmit} className="report-form">
                <div className="form-group">
                  <label htmlFor="report-text">Issue Description</label>
                  <textarea
                    id="report-text"
                    value={reportText}
                    onChange={(e) => setReportText(e.target.value)}
                    placeholder="What went wrong? Please provide as much detail as possible..."
                    rows={6}
                    disabled={isSubmitting}
                    required
                  />
                </div>
              </form>
            </div>
            
            <div className="dialog-footer">
              <button 
                type="button" 
                className="btn btn-secondary" 
                onClick={handleClose}
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button 
                type="submit" 
                className="btn btn-primary" 
                onClick={handleSubmit}
                disabled={!reportText.trim() || isSubmitting}
              >
                {isSubmitting ? (
                  <span className="btn-loading">
                    <span className="spinner"></span>
                    Sending...
                  </span>
                ) : (
                  'Send Report'
                )}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}