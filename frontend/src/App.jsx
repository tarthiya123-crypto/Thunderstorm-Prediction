import { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
  console.log("Analyze clicked");

  if (!file) {
    alert("Select an INSAT file first");
    return;
  }

  try {
    const formData = new FormData();
    formData.append("file", file);

    console.log("Sending request...");

    const response = await fetch(
      "http://127.0.0.1:8000/predict",
      {
        method: "POST",
        body: formData,
      }
    );

    console.log("Status:", response.status);

    const data = await response.json();

    console.log("Response:", data);

    setResult(data);

  } catch (err) {
    console.error("ERROR:", err);
  }
};
  return (
    <div style={{ padding: "30px" }}>
      <h1>Thunderstorm Early Warning System</h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload}>
        Analyze
      </button>

      {result && (
  <div style={{ marginTop: "30px" }}>
    <h2>Results</h2>
    <MapContainer
  center={[20, 75]}
  zoom={4}
  style={{ height: "500px", width: "100%" }}
>
  <TileLayer
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
  />

  {result.alerts.map((alert, index) => (
    <Marker
      key={index}
      position={[alert.Latitude, alert.Longitude]}
    >
      <Popup>
        <b>Cloud {alert.CloudID}</b>
        <br />
        Probability:
        {" "}
        {(alert.Probability * 100).toFixed(0)}%
      </Popup>
    </Marker>
  ))}
</MapContainer>
    <p>Total Clouds: {result.total_clouds}</p>

    <p>
      Thunderstorm Clouds: {result.thunderstorm_clouds}
    </p>

    <p>
      Highest Probability:
      {(result.highest_probability * 100).toFixed(0)}%
    </p>

    <h2>Active Alerts</h2>

    <table border="1" cellPadding="8">
      <thead>
        <tr>
          <th>Cloud ID</th>
          <th>Probability</th>
          <th>Latitude</th>
          <th>Longitude</th>
        </tr>
      </thead>

      <tbody>
        {result.alerts.map((alert, index) => (
          <tr key={index}>
            <td>{alert.CloudID}</td>
            <td>
              {(alert.Probability * 100).toFixed(0)}%
            </td>
            <td>{alert.Latitude.toFixed(2)}</td>
            <td>{alert.Longitude.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)}
    </div>
  );
}
export default App;