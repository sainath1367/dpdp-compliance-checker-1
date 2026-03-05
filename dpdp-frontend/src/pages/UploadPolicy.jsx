import Sidebar from "../components/Sidebar";
import { useState } from "react";
import API from "../services/api";

function UploadPolicy() {

  const [file, setFile] = useState(null);
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // File Upload Analysis
  const handleUpload = async () => {

    if (!file) {
      alert("Please upload a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {

      setLoading(true);

      const response = await API.post("/analyze-policy", formData);

      setResult(response.data);

    } catch (error) {

      console.error(error);
      alert("Error analyzing policy");

    }

    setLoading(false);

  };

  // URL Analysis
  const handleURLAnalysis = async () => {

    if (!url) {
      alert("Enter website URL");
      return;
    }

    try {

      setLoading(true);

      const response = await API.post("/analyze-url", {
        url: url
      });

      setResult(response.data);

    } catch (error) {

      console.error(error);
      alert("Error analyzing URL");

    }

    setLoading(false);

  };

  return (

    <div className="flex">

      {/* Sidebar */}

      <Sidebar />

      {/* Main Content */}

      <div className="ml-64 p-10 w-full bg-gray-100 min-h-screen">

        <h1 className="text-3xl font-bold mb-8">
          DPDP Act 2023 Compliance Checker
        </h1>

        {/* Upload Section */}

        <div className="bg-white p-6 rounded-xl shadow mb-6">

          <h2 className="text-lg font-semibold mb-3">
            Upload Privacy Policy File
          </h2>

          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button
            className="ml-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
            onClick={handleUpload}
          >
            Analyze File
          </button>

        </div>

        {/* URL Analysis */}

        <div className="bg-white p-6 rounded-xl shadow mb-6">

          <h2 className="text-lg font-semibold mb-3">
            Analyze Website Privacy Policy URL
          </h2>

          <input
            type="text"
            placeholder="Enter privacy policy URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="border p-2 w-96 rounded"
          />

          <button
            className="ml-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
            onClick={handleURLAnalysis}
          >
            Analyze URL
          </button>

        </div>

        {/* Loading */}

        {loading && (

          <div className="text-blue-600 font-semibold mb-6">
            AI analyzing privacy policy...
          </div>

        )}

        {/* Results */}

        {result && (

          <div className="bg-white p-6 rounded-xl shadow">

            {/* Score */}

            <h2 className="text-2xl font-bold mb-4">
              Compliance Score: {result.overall_score}%
            </h2>

            {/* Risk Level */}

            <div className="mb-4">

              <p className="font-semibold mb-2">
                Risk Level
              </p>

              {result.risk_level === "Low Risk" && (
                <div className="bg-green-100 text-green-700 p-3 rounded w-48">
                  Low Risk
                </div>
              )}

              {result.risk_level === "Medium Risk" && (
                <div className="bg-yellow-100 text-yellow-700 p-3 rounded w-48">
                  Medium Risk
                </div>
              )}

              {result.risk_level === "High Risk" && (
                <div className="bg-red-100 text-red-700 p-3 rounded w-48">
                  High Risk
                </div>
              )}

            </div>

            {/* Missing Clauses */}

            <h3 className="font-semibold mt-6">
              Missing DPDP Clauses
            </h3>

            <ul className="list-disc ml-6 mt-2">

              {result.missing_clauses.map((clause, index) => (

                <li key={index}>{clause}</li>

              ))}

            </ul>

            {/* Recommendations */}

            {result.recommendations && (

              <>

                <h3 className="font-semibold mt-6">
                  AI Recommendations
                </h3>

                <ul className="list-disc ml-6 mt-2">

                  {result.recommendations.map((rec, index) => (

                    <li key={index}>{rec}</li>

                  ))}

                </ul>

              </>

            )}

            {/* Chart */}

            <h3 className="text-xl font-bold mt-8">
              Compliance Chart
            </h3>

            <img
              src={`http://127.0.0.1:8000/${result.graph_path}`}
              alt="Compliance Chart"
              className="mt-4 w-full max-w-3xl border rounded"
            />

          </div>

        )}

      </div>

    </div>

  );

}

export default UploadPolicy;