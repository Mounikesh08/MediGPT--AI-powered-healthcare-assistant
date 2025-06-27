import React from "react";
import ChatBox from "./components/ChatBox";
import PdfUpload from "./components/PdfUpload";
import "./App.css";

function App() {
  return (
    <div className="app-container">
      <h1>MediGPT 💊</h1>
      <PdfUpload />
      <ChatBox />
    </div>
  );
}

export default App;
