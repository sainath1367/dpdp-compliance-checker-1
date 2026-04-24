import Sidebar from "../components/Sidebar";
import { useState, useEffect } from "react";
import API from "../services/api";

function UploadPolicy({ user }) {
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [useAI, setUseAI] = useState(true); // Default to AI mode

  // Debug: Log when component mounts
  useEffect(() => {
    console.log("✅ UploadPolicy component mounted", { user });
  }, [user]);

  const resetStatus = () => {
    setError(null);
    setSuccess(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please upload a file to analyze.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      resetStatus();

      const response = await API.post("/analyze-policy", formData);
      setResult(response.data);
      setSuccess(`File analyzed successfully: ${file.name}`);
    } catch (error) {
      console.error(error);
      setError("Error analyzing policy. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleURLAnalysis = async () => {
    if (!url.trim()) {
      setError("Please enter a valid website URL.");
      return;
    }

    try {
      setLoading(true);
      resetStatus();

      const response = await API.post("/analyze-url", { url: url.trim() });
      setResult(response.data);
      setSuccess("Website privacy policy analyzed successfully.");
    } catch (error) {
      console.error(error);
      const backendMessage = error?.response?.data?.detail || error?.response?.data?.error || error?.message;
      setError(backendMessage || "Error analyzing URL. Please check the URL and try again.");
    } finally {
      setLoading(false);
    }
  };

  const getApiBaseUrl = () => {
    return import.meta.env.VITE_API_BASE_URL || `${window.location.protocol}//${window.location.hostname}:8000`;
  };

  const handleDownloadReport = () => {
    const apiBaseUrl = getApiBaseUrl();
    window.open(`${apiBaseUrl}/download-report`, "_blank");
  };

  const getGraphPath = () => {
    const apiBaseUrl = getApiBaseUrl();
    return `${apiBaseUrl}/${result.graph_path}`;
  };

  const getRiskClasses = (risk) => {
    if (risk === "Low Risk") return "border-green-200 bg-emerald-50 text-emerald-900";
    if (risk === "Medium Risk") return "border-yellow-200 bg-amber-50 text-amber-900";
    return "border-red-200 bg-rose-50 text-rose-900";
  };

  return (
    <div className="flex min-h-screen bg-slate-100 dark:bg-slate-950 transition-colors duration-500">
      <Sidebar />

      <main className="ml-72 flex-1 p-8 xl:p-10">
        <div className="bg-white p-8 rounded-lg">
          <h1 className="text-3xl font-bold">DPDP Compliance Policy Analyzer</h1>
          <p className="text-gray-600 mt-4">Upload a policy or analyze a URL to check DPDP compliance.</p>
          
          <div className="mt-8 space-y-6">
            {/* AI Mode Toggle */}
            <div className="p-4 border border-gray-300 rounded-lg bg-blue-50">
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={useAI}
                  onChange={(e) => setUseAI(e.target.checked)}
                  className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                />
                <span className="text-lg font-semibold text-blue-800">Use AI Mode (Gemini)</span>
              </label>
              <p className="text-sm text-blue-600 mt-1">
                {useAI ? "Using advanced AI analysis for better accuracy" : "Using local model for offline analysis"}
              </p>
            </div>
            {/* FILE UPLOAD */}
            <div className="p-6 border border-gray-300 rounded-lg">
              <h2 className="text-xl font-semibold mb-4">Upload Policy File</h2>
              <input
                type="file"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="block w-full p-2 border border-gray-300 rounded"
              />
              <button
                onClick={handleUpload}
                disabled={loading}
                className="mt-4 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? "Analyzing..." : "Analyze File"}
              </button>
            </div>

            {/* URL ANALYSIS */}
            <div className="p-6 border border-gray-300 rounded-lg">
              <h2 className="text-xl font-semibold mb-4">Analyze URL</h2>
              <input
                type="text"
                placeholder="https://example.com/privacy"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="block w-full p-2 border border-gray-300 rounded"
              />
              <button
                onClick={handleURLAnalysis}
                disabled={loading}
                className="mt-4 px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? "Analyzing..." : "Analyze URL"}
              </button>
            </div>

            {/* STATUS MESSAGES */}
            {error && (
              <div className="p-4 bg-red-100 border border-red-400 text-red-800 rounded">
                ❌ {error}
              </div>
            )}
            {success && (
              <div className="p-4 bg-green-100 border border-green-400 text-green-800 rounded">
                ✅ {success}
              </div>
            )}

            {/* RESULTS */}
            {result && (
              <div className="p-6 border border-gray-300 rounded-lg bg-gray-50">
                <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>
                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div className="p-4 bg-white rounded border">
                    <p className="text-gray-600">Score</p>
                    <p className="text-3xl font-bold">{result.overall_score}%</p>
                  </div>
                  <div className="p-4 bg-white rounded border">
                    <p className="text-gray-600">Risk Level</p>
                    <p className="text-xl font-semibold">{result.risk_level}</p>
                  </div>
                  <div className="p-4 bg-white rounded border">
                    <p className="text-gray-600">Missing Clauses</p>
                    <p className="text-3xl font-bold">{result.missing_clauses?.length || 0}</p>
                  </div>
                </div>

                {/* Clause Analysis */}
                {result.clause_analysis && result.clause_analysis.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-xl font-semibold mb-3">Clause Analysis</h3>
                    <div className="space-y-2">
                      {result.clause_analysis.map((clause, index) => (
                        <div key={index} className="p-3 bg-white rounded border">
                          <div className="flex justify-between items-center">
                            <span className="font-medium">{clause.clause}</span>
                            <span className={`px-2 py-1 rounded text-sm ${
                              clause.status === 'Compliant' ? 'bg-green-100 text-green-800' :
                              clause.status === 'Partial' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {clause.status} ({clause.score}%)
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mt-1">{clause.reason}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Recommendations */}
                {result.recommendations && result.recommendations.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-xl font-semibold mb-3">Recommendations</h3>
                    <ul className="list-disc list-inside space-y-1">
                      {result.recommendations.map((rec, index) => (
                        <li key={index} className="text-gray-700">{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <button
                  onClick={handleDownloadReport}
                  className="px-6 py-2 bg-orange-600 text-white rounded hover:bg-orange-700"
                >
                  📄 Download PDF Report
                </button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default UploadPolicy;
