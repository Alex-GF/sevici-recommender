import "leaflet/dist/leaflet.css";
import "../static/css/filterButton.css";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import FormGenerator from "../components/formGenerator/formGenerator";
import { filterStationsInputs } from "../forms/filterStationsForm";
import { useRef, useEffect, useState } from "react";
import CompassLoader from "../components/compassLoader";
import useQuery from "../hooks/useQuery";

const Home = () => {
  const query = useQuery();

  let [stations, setStations] = useState([]);
  let [dataLoaded, setDataLoaded] = useState(false);
  let [firstLoad, setFirstLoad] = useState(true);
  let [filterValues, setFilterValues] = useState({});

  const filterFormRef = useRef(null);

  function handleSubmit({ values }) {

    if (dataLoaded && !filterFormRef.current.validate()) return;

    setDataLoaded(false);

    let query = "http://localhost:8000/api/stations?";

    for (let key in values) {
      if (values[key]) {
        if (key === "hour"){
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
        setStations(data.results);
        setFilterValues(values);
        setDataLoaded(true);
      })
      .catch((error) => console.log(error));
  }

  useEffect(() => {
    if(dataLoaded){
      document.getElementsByClassName("class-form")[0].style.justifyContent = "start";
    }
    if(firstLoad){
      handleSubmit({ values: {} });
      setFirstLoad(false);
    }
  }, [dataLoaded]);

  useEffect(() => {
    filterStationsInputs.forEach((input) => {
      if (filterValues[input.name]) {
        input.defaultValue = filterValues[input.name];
      }
    });
  }, [filterValues]);

  return (
    <div className="flex h-screen w-screen flex-col items-center justify-center bg-slate-200 bg-opacity-80 bg-[radial-gradient(#444cf7_0.5px,_transparent_0.5px),_radial-gradient(#444cf7_0.5px,_#e5e5f7_0.5px)] bg-[length:20px_20px]">
      {!dataLoaded ? (
        <CompassLoader />
      ) : (
        <div className="flex h-[80%] w-[90%] flex-col-reverse items-center justify-between lg:w-[80%] lg:flex-row">
          <div className="mt-10 flex h-auto w-[80%] flex-col items-center justify-center rounded-md bg-white p-5 pt-12 lg:mt-0 lg:w-1/4">
            <h2 className="h-50% py-5 text-xl font-extrabold text-black underline underline-offset-4 lg:text-4xl">
              Filtros
            </h2>
            <FormGenerator
              ref={filterFormRef}
              inputs={filterStationsInputs}
              onSubmit={handleSubmit}
              childrenPosition={-1}
              buttonText="Filtrar"
              buttonClassName="filterButton"
              listenEnterKey
              scrollable
            />
          </div>
          <div className="h-full w-full lg:w-[70%]">
            <MapContainer
              center={[37.38283, -5.97317]}
              zoom={13}
              scrollWheelZoom={true}
              className="h-full w-full"
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              {stations &&
                stations.map((station, index) => {
                  let xCoord = station.station.location.coordinates[1];
                  let yCoord = station.station.location.coordinates[0];

                  return (
                    <Marker position={[xCoord, yCoord]} key={index}>
                      <Popup>
                        <strong>Estación nº {station.station.number}: {station.station.address}</strong>
                        <br /> <br />
                        Bicicletas disponibles: {
                          station.available_bikes
                        } 
                        <br /> <br />
                        Capacidad de la estación: {
                          station.total_capacity
                        }
                        <br /> <br />
                        Estado: {station.is_open? "Abierta" : "Cerrada"}
                      </Popup>
                    </Marker>
                  );
                })}
            </MapContainer>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
