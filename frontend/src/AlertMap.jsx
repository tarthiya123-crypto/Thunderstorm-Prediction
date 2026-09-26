import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { Icon } from "leaflet";

const redIcon = new Icon({
  iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

function AlertMap({ alerts }) {
  return (
    <MapContainer
      center={[20, 80]}
      zoom={4}
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer
        attribution="OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {alerts.map((alert, index) => (
        <Marker
          key={index}
          position={[alert.Latitude, alert.Longitude]}
          icon={redIcon}
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
  );
}

export default AlertMap;