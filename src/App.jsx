import React from 'react';
import { invoke } from "@tauri-apps/api/core";

import Home from './pages/Home/Home';
import './app.css';

function App() {
  return (
    <div className="app">
      <main id="main-content" className="main-content">
        <Home />
      </main>
    </div>
  );
}

export default App;
