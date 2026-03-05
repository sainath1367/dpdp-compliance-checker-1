import { Link } from "react-router-dom";
import { useState, useEffect } from "react";

function Navbar() {

  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {

    if (darkMode) {
      document.body.classList.add("dark");
    } else {
      document.body.classList.remove("dark");
    }

  }, [darkMode]);

  return (

    <div className="bg-gradient-to-r from-blue-700 to-indigo-800 text-white p-4 flex justify-between items-center">

      <h1 className="text-xl font-bold">
        DPDP Compliance Checker
      </h1>

      <div className="flex items-center gap-6">

        <Link to="/dashboard">Dashboard</Link>
        <Link to="/upload">Analyze Policy</Link>
        <Link to="/reports">Reports</Link>

        {/* Theme Toggle Button */}

        <button
  onClick={() => setDarkMode(!darkMode)}
  className="text-2xl bg-white/10 p-2 rounded-full hover:bg-white/20 transition"
>
  {darkMode ? "☀️" : "🌙"}
</button>
      </div>

    </div>

  );

}

export default Navbar;