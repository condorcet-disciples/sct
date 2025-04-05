import React from "react";
import "./App.css";

function App() {
  return (
    <div className="app">
      <header className="navbar">
        <div className="logo" onClick={() => (window.location.href = "/")}>
          🗳️
        </div>
        <div className="nav-links">
          <a href="/about">About</a>
          <a href="https://github.com/your-repo" target="_blank" rel="noreferrer">
            GitHub
          </a>
        </div>
      </header>
      <main className="main-content">
        <h1>Election Generator</h1>
        <p className="subtitle">
          A tool to create elections and analyze different voting systems
        </p>
        <button
          className="create-btn"
          onClick={() => window.open("/create", "_blank")}
        >
          Create an Election
        </button>
      </main>
    </div>
  );
}

export default App;