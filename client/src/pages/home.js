import { useNavigate } from "react-router-dom";

export default function Home() {

  const navigator = useNavigate()

  return (
    <div className="flex h-screen w-screen flex-col items-center justify-center bg-slate-200 bg-opacity-80 bg-[radial-gradient(#444cf7_0.5px,_transparent_0.5px),_radial-gradient(#444cf7_0.5px,_#e5e5f7_0.5px)] bg-[length:20px_20px]">
      <img
        src={require("../static/icons/bicicleta.png")}
        alt="Logo"
        className="mb-10 h-[300px] w-[300px]"
      />
      <h1 className="text-center text-4xl font-bold text-slate-900 underline underline-offset-2 mb-3">
        Bienvenido a al analizador de SEVICI
      </h1>
      <h2 className="text-center text-2xl font-thin text-slate-900">
        Selecciona uno de nuestros servicios a continuación
      </h2>
      <div className="mt-14 flex w-3/4 flex-col justify-evenly lg:flex-row">
        <button className="filterButton" onClick={() => navigator("/filter")}>Filtrar</button>
        <button className="filterButton" onClick={() => navigator("/predictor")}>Predecir</button>
        <button className="filterButton" onClick={() => navigator("/research")}>Investigar</button>
      </div>
    </div>
  );
}
