import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import CreatePage from "./pages/CreateInvite";
import JoinPage from "./pages/JoinInvite";
import Header from "./components/Header"; // Optional: Add a header component
import "./App.css";

function App() {
  // Example: Replace with actual logged-in user data
  const username = "John Doe";

  return (
    <Router>
      <div>
        {/* Fixed top header */}
        <div className="fixed-top">
          <div className="absolute-inset">
            {/* <Header username={username} /> Optional: Add a header */}
          </div>
        </div>

        {/* Main content with routing */}
        <div className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/create" element={<CreatePage />} />
            <Route path="/join" element={<JoinPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
