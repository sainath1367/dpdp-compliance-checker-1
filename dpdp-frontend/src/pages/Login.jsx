import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { signInWithPopup } from "firebase/auth";
import { auth, provider } from "../firebase";

function Login() {

  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  // Check for existing session on load
  useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if (savedUser) {
      setUser(JSON.parse(savedUser));
      navigate("/dashboard");
    }
  }, [navigate]);

  const handleGoogleLogin = async () => {
    try {
      setLoading(true);
      const result = await signInWithPopup(auth, provider);

      // Get user info
      const userData = {
        uid: result.user.uid,
        email: result.user.email,
        displayName: result.user.displayName,
        photoURL: result.user.photoURL,
        emailVerified: result.user.emailVerified
      };

      // Save to localStorage for session persistence
      localStorage.setItem("user", JSON.stringify(userData));
      setUser(userData);

      // Optional: Send token to backend for verification
      // const token = await result.user.getIdToken();
      // await axios.post("http://localhost:8000/api/auth/google", { token });

      navigate("/dashboard");

    } catch (error) {
      console.error("Google login error:", error);
      alert("Google login failed. Please try again.");
    } finally {
      setLoading(false);
    }
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

        <p className="text-gray-300 text-center mb-8">
          AI Powered Privacy Compliance
        </p>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleGoogleLogin}
          disabled={loading}
          className="w-full bg-white text-gray-800 p-3 rounded-lg font-semibold shadow-lg flex items-center justify-center gap-3 hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <div className="spinner w-5 h-5 border-2 border-gray-300 border-t-gray-800 rounded-full animate-spin"></div>
          ) : (
            <>
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Sign in with Google
            </>
          )}
        </motion.button>

        <div className="mt-6 text-center">
          <p className="text-gray-400 text-sm">
            Secure authentication powered by Google OAuth
          </p>
        </div>

      </motion.div>

    </div>
  );
}

export default Login;