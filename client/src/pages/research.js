import RegressionGraph from "../components/graphs/RegressionGraph";
import { predictStationsInputs } from "../forms/predictStationForm";
import { useRef, useEffect, useState } from "react";
import FormGenerator from "../components/formGenerator/formGenerator";
import MeanGraph from "../components/graphs/MeanGraph";
import ReturnButton from "../components/returnButton";

export default function Research() {
  let [filterValues, setFilterValues] = useState({});
  let [filtered, setFiltered] = useState(false);

  const predictFormRef = useRef(null);

  function handleSubmit({ values }) {
    setFilterValues(values);
    setFiltered(true);
  }

  useEffect(() => {
    document.getElementsByClassName("class-form")[0].style.justifyContent =
      "start";
    
    document.title = "Bicicator - Investigación"
    document.querySelector('meta[name="description"]').setAttribute("content", "Servicio de investigación de bicicator. Aquí puedes comparar cómo rinden los distintos modelos de predicción en las estaciones de SEVICI.");
  }, [filtered]);

  useEffect(() => {
    predictStationsInputs.forEach((input) => {
      if (predictFormRef[input.name]) {
        input.defaultValue = filterValues[input.name];
      }
    });
  }, [filterValues]);

  return (
    <div className="relative flex h-screen w-screen flex-col items-center justify-center bg-slate-200 bg-opacity-80 bg-[radial-gradient(#444cf7_0.5px,_transparent_0.5px),_radial-gradient(#444cf7_0.5px,_#e5e5f7_0.5px)] bg-[length:20px_20px]">
      <ReturnButton/>
      <div className="flex h-[80%] w-[90%] flex-col-reverse items-center justify-between lg:w-[80%] lg:flex-row">
        <div className="mt-10 flex h-auto w-[80%] flex-col items-center justify-center rounded-md bg-white p-5 pt-12 lg:mt-0 lg:w-1/4">
          <h2 className="h-50% py-5 text-xl font-extrabold text-black underline underline-offset-4 lg:text-4xl">
            Parámetros
          </h2>
          <FormGenerator
            ref={predictFormRef}
            inputs={predictStationsInputs}
            onSubmit={handleSubmit}
            childrenPosition={-1}
            buttonText="Predecir"
            buttonClassName="filterButton"
            listenEnterKey
            scrollable
          />
        </div>
        <div className="flex h-full w-full flex-col items-center justify-evenly lg:w-[70%]">
          {filtered ? (
            <>
              <RegressionGraph
                date={filterValues.date}
                hour={filterValues.hour}
                stationNumber={filterValues.stationNumber}
                width={1000}
                height={350}
              />
              <MeanGraph
                date={filterValues.date}
                hour={filterValues.hour}
                stationNumber={filterValues.stationNumber}
                width={1000}
                height={350}
              />
            </>
          ) : (
            <div className="flex h-2/4 w-[90%] flex-col items-center justify-evenly rounded-md bg-white px-10">
              <div className="flex items-center justify-center">
                <h2 className="text-center text-3xl font-bold underline underline-offset-2">
                  ¡BIENVENIDO AL PREDICTOR DE ESTACIONES!
                </h2>
              </div>
              <div className="flex items-center justify-center">
                <p className="text-center text-lg">
                  Utiliza el menu de parámetros para estudiar la evolucion de
                  las bicis disponibles en una parada de SEVICI y predecir el
                  número de paradas que estarán disponibles en la próxima semana
                  usando dos métodos:{" "}
                  <span className="font-bold">
                    predicción por media y por regresión
                  </span>
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
