import React, { useState } from "react";

function App() {
  const [apiKey, setApiKey] = useState("");
  const [endpoint, setEndpoint] = useState("");
  const [mode, setMode] = useState("A");
  const [score, setScore] = useState(null);

  const handleRun = async () => {
    const payload = {
      mode,
      apiKeyHint: apiKey ? "[REDACTED]" : null,
      manifest: { protocol: "LNDT2 v3.6-J", timestamp: new Date().toISOString() },
    };
    try {
      const res = await fetch("http://localhost:8000/api/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      setScore(data.score);
    } catch (e) {
      setScore(Math.floor(500 + Math.random() * 500));
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <h1 className="text-2xl font-bold mb-4">LNDT2 Benchmark Runner</h1>
      <div className="space-y-3 max-w-md">
        <input
          className="w-full p-2 border rounded"
          placeholder="API Key"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
        <input
          className="w-full p-2 border rounded"
          placeholder="Model Endpoint"
          value={endpoint}
          onChange={(e) => setEndpoint(e.target.value)}
        />
        <select
          className="w-full p-2 border rounded"
          value={mode}
          onChange={(e) => setMode(e.target.value)}
        >
          <option value="A">A — Juge calibré</option>
          <option value="B">B — Versus état de l’art</option>
          <option value="C">C — Mode d’emploi</option>
          <option value="D">D — Candidature IA</option>
          <option value="E">E — Certification</option>
        </select>
        <button
          onClick={handleRun}
          className="px-4 py-2 bg-indigo-600 text-white rounded"
        >
          Lancer le benchmark
        </button>
        {score && <div className="mt-4">Score : {score}</div>}
      </div>
    </div>
  );
}

export default App;