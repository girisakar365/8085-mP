import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import React from 'react';
// ...removed ThemeProvider import...
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);