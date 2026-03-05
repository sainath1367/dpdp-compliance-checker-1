import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import UploadPolicy from "./pages/UploadPolicy";
import Reports from "./pages/Reports";
import Navbar from "./components/Navbar";

function App() {

  return (

    <BrowserRouter>

      <Navbar />

      <Routes>

        <Route path="/" element={<Login />} />

        <Route path="/dashboard" element={<Dashboard />} />

        <Route path="/upload" element={<UploadPolicy />} />

        <Route path="/reports" element={<Reports />} />

      </Routes>

    </BrowserRouter>

  );

}

export default App;