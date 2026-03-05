import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {

    if (!email || !password) {
      alert("Enter email and password");
      return;
    }

    navigate("/dashboard");
  };

  return (

    <div className="h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-purple-900 to-black">

      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}

        className="backdrop-blur-lg bg-white/10 border border-white/20 p-10 rounded-2xl shadow-2xl w-96"
      >

        <h1 className="text-3xl font-bold text-white text-center mb-6">
          DPDP Compliance Checker
        </h1>

        <p className="text-gray-300 text-center mb-6">
          AI Powered Privacy Compliance
        </p>

        <input
          type="email"
          placeholder="Enter Email"
          className="w-full p-3 mb-4 rounded bg-white/20 text-white placeholder-gray-300"
          onChange={(e)=>setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Enter Password"
          className="w-full p-3 mb-6 rounded bg-white/20 text-white placeholder-gray-300"
          onChange={(e)=>setPassword(e.target.value)}
        />

        <motion.button

          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}

          onClick={handleLogin}

          className="w-full bg-gradient-to-r from-blue-500 to-purple-600 p-3 rounded text-white font-semibold shadow-lg"
        >
          Login
        </motion.button>

      </motion.div>

    </div>
  );
}

export default Login;