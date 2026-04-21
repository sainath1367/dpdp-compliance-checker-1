import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState, useEffect } from "react";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import UploadPolicy from "./pages/UploadPolicy";
import Reports from "./pages/Reports";
import Navbar from "./components/Navbar";

function App() {
  const [user, setUser] = useState(null);

  // Check for existing session on app load
  useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUser(null);
  };

  return (
    <BrowserRouter>
      <Navbar user={user} onLogout={handleLogout} />
      <Routes>
        <Route path="/" element={<Login setUser={setUser} />} />
        <Route path="/dashboard" element={<Dashboard user={user} />} />
        <Route path="/upload" element={<UploadPolicy user={user} />} />
        <Route path="/reports" element={<Reports user={user} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;