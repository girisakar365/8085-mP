import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './index.css';
// Import settings store to trigger initialization
import './features/settings/stores/settingsStore';

const root = createRoot(document.getElementById('root'));
root.render(<App />);