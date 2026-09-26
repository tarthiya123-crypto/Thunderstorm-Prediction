import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      alert("Select an INSAT file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
      "http://127.0.0.1:8000/predict",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await response.json();

    setResult(data);
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>Thunderstorm Early Warning System</h1>

      <input
        type="file"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <br />
      <br />

      <button onClick={handleUpload}>
        Analyze
      </button>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h2>Results</h2>

          <p>
            Total Clouds:
            {" "}
            {result.total_clouds}
          </p>

          <p>
            Thunderstorm Clouds:
            {" "}
            {result.thunderstorm_clouds}
          </p>

          <p>
            Highest Probability:
            {" "}
            {(result.highest_probability * 100).toFixed(0)}%
          </p>
        </div>
      )}
    </div>
  );
}

export default App;