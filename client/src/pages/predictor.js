import "leaflet/dist/leaflet.css";
import "../static/css/filterButton.css";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMapEvent,
} from "react-leaflet";
import FormGenerator from "../components/formGenerator/formGenerator";
import { bestStationPredictorInputs } from "../forms/bestStationPredictorForm";
import { useRef, useEffect, useState } from "react";
import CompassLoader from "../components/compassLoader";
import RoutedMap from "../components/maps/RoutedMap";

function MovingMarker({ position, setPosition }) {
  const markerRef = useRef(null);
  const map = useMapEvent("click", (e) => {
    setPosition([e.latlng.lat, e.latlng.lng]);
  });

  return <Marker position={position} ref={markerRef}></Marker>;
}

const Predictor = () => {
  let [position, setPosition] = useState([37.38283, -5.97317]);
  let [positionLoaded, setPositionLoaded] = useState(false);
  let [predicted, setPredicted] = useState(false);
  let [predictedStations, setPredictedStations] = useState([]);
  let [destinationStation, setDestinationStation] = useState(null);
  const bestStationFormRef = useRef(null);

  function handleSubmit({ values }) {
    if (!bestStationFormRef.current.validate()) return;

    setPositionLoaded(false);
    setPredicted(false);
    setDestinationStation(null)

    values["latitude"] = position[0];
    values["longitude"] = position[1];

    values["method"] = values["method"] === "Media" ? "mean" : "linear";

    let query = "http://localhost:8000/api/predictors/nearby?";

    for (let key in values) {
      if (values[key]) {
        if (key === "hour") {
          query += `${key}=${values[key]}:00&`;
        } else {
          query += `${key}=${values[key]}&`;
        }
      }
    }

    query = query.slice(0, -1);

    fetch(query)
      .then((response) => response.json())
      .then((data) => {
        setPredictedStations(data);
        setPositionLoaded(false);
        setPredicted(true);
      })
      .catch((error) => console.log(error));
  }

  useEffect(() => {
    document.getElementsByClassName("class-form")[0].style.justifyContent =
      "start";
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setPosition([position.coords.latitude, position.coords.longitude]);
        setPositionLoaded(true);
      },
      (error) => {
        setPositionLoaded(true);
      }
    );
  }, []);

  useEffect(() => {}, [destinationStation]);

  return (
    <div className="flex h-screen w-screen flex-col items-center justify-center bg-slate-200 bg-opacity-80 bg-[radial-gradient(#444cf7_0.5px,_transparent_0.5px),_radial-gradient(#444cf7_0.5px,_#e5e5f7_0.5px)] bg-[length:20px_20px]">
      <div className="flex h-[80%] w-[90%] flex-col-reverse items-center justify-between lg:w-[80%] lg:flex-row">
        <div className="mt-10 flex h-auto w-[80%] flex-col items-center justify-center rounded-md bg-white p-5 pt-12 lg:mt-0 lg:w-1/4">
          <h2 className="h-50% py-5 text-xl font-extrabold text-black underline underline-offset-4 lg:text-4xl">
            Parámetros:
          </h2>
          <FormGenerator
            ref={bestStationFormRef}
            inputs={bestStationPredictorInputs}
            onSubmit={handleSubmit}
            childrenPosition={-1}
            buttonText="Recomiéndame"
            buttonClassName="filterButton"
            scrollable
          />
        </div>
        <div className="flex h-full w-full items-center justify-center lg:w-[70%]">
          {!positionLoaded && !predicted ? (
            <CompassLoader />
          ) : !predicted && destinationStation === null ? (
            <MapContainer
              center={position}
              minZoom={2}
              maxZoom={17}
              zoom={position === [37.38283, -5.97317] ? 12 : 17}
              scrollWheelZoom={true}
              className="h-full w-full"
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <MovingMarker position={position} setPosition={setPosition} />
            </MapContainer>
          ) : predicted && destinationStation === null ? (
            <MapContainer
              center={position}
              minZoom={2}
              maxZoom={17}
              zoom={position === [37.38283, -5.97317] ? 12 : 17}
              scrollWheelZoom={true}
              className="h-full w-full"
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Marker position={position}>
                      <Popup>
                        <strong>
                          Tu ubicación
                        </strong>
                      </Popup>
                    </Marker>
              {predictedStations &&
                predictedStations.map((station, index) => {
                  let xCoord = station.station.location.coordinates[1];
                  let yCoord = station.station.location.coordinates[0];

                  return (
                    <Marker position={[xCoord, yCoord]} key={index} eventHandlers={{
                      click: () => {
                        setDestinationStation(station);
                      }
                    }}>
                      <Popup>
                        <strong>
                          Estación nº {station.station.number}:{" "}
                          {station.station.address}
                        </strong>
                        <br /> <br />
                        Predicción: {station.prediction.toFixed(2)} bicis
                        disponibles
                      </Popup>
                    </Marker>
                  );
                })}
            </MapContainer>
          ) : (
            <RoutedMap
              originCoords={{
                lat: position[0],
                lng: position[1],
              }}
              destinationCoords={{
                lat: destinationStation.station.location.coordinates[1],
                lng: destinationStation.station.location.coordinates[0],
              }}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default Predictor;
