import "leaflet/dist/leaflet.css";
import "../static/css/filterButton.css";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import FormGenerator from "../components/formGenerator/formGenerator";
import { filterStationsInputs } from "../forms/filterStationsForm";
import { useRef, useEffect } from "react";

const Home = () => {
  const filterFormRef = useRef(null);

  function handleSubmit({ values }) {
    if (!filterFormRef.current.validate()) return;
    console.log(values);
  }

  useEffect(() => {
    document.getElementsByClassName("class-form")[0].style.justifyContent = "start";
  }, []);

  return (
    <div className="flex h-screen w-screen flex-col items-center justify-center bg-slate-200 bg-opacity-80 bg-[radial-gradient(#444cf7_0.5px,_transparent_0.5px),_radial-gradient(#444cf7_0.5px,_#e5e5f7_0.5px)] bg-[length:20px_20px]">
      <div className="flex h-[80%] lg:w-[80%] w-[90%] lg:flex-row flex-col-reverse items-center justify-between">
        <div className="flex h-auto flex-col lg:w-1/4 w-[80%] lg:mt-0 mt-10 items-center justify-center rounded-md bg-white p-5 pt-12">
          <h2 className="h-50% py-5 text-xl font-extrabold text-black underline underline-offset-4 lg:text-4xl">
            Filtros:
          </h2>
          <FormGenerator
            ref={filterFormRef}
            inputs={filterStationsInputs}
            onSubmit={handleSubmit}
            childrenPosition={-1}
            buttonText="Filtrar"
            buttonClassName="filterButton"
            scrollable
          />
        </div>
        <div className="h-full lg:w-[70%] w-full">
          <MapContainer
            center={[37.3828300, -5.9731700]}
            zoom={13}
            scrollWheelZoom={true}
            className="h-full w-full"
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <Marker position={[37.3828300, -5.9731700]}>
              <Popup>
                A pretty CSS3 popup. <br /> Easily customizable.
              </Popup>
            </Marker>
          </MapContainer>
        </div>
      </div>
    </div>
  );
};

export default Home;
