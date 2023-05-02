import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import CompassLoader from "../components/compassLoader";

export default function Graphs() {
  let [points, setPoints] = useState([]);
  let [linearFunctionPoints, setLinearFunctionPoints] = useState([]);
  let [dataLoaded, setDataLoaded] = useState(false);
  let [firstLoad, setFirstLoad] = useState(true);
  let [yLimits, setYLimits] = useState([0, 50]);

  function handleSubmit({ values }) {
    setDataLoaded(false);

    let query = "http://localhost:8000/api/station/?";

    for (let key in values) {
      if (values[key]) {
        query += `${key}=${values[key]}&`;
      }
    }

    query = query.slice(0, -1);

    fetch(query)
      .then((response) => response.json())
      .then((data) => {
        let sortedListOfPoints = data.evolution.sort((a, b) => a.x - b.x);
        let maxY = Math.max(...sortedListOfPoints.map((point) => point.y)) + 5;
        let minY = Math.min(...sortedListOfPoints.map((point) => point.y)) - 5;

        setYLimits([minY, maxY]);

        setPoints(sortedListOfPoints);

        let linearPoints = [];

        let originTimestamp = sortedListOfPoints[0].x;

        for (let point of sortedListOfPoints) {
          linearPoints.push({
            x: point.x,
            y:
              data.linear_function.coef * (point.x - originTimestamp) +
              data.linear_function.intercept,
          });
        }
        console.log(data.linear_function.coef, data.linear_function.intercept);
        for (let i = 1; i <= 7; i++) {
          let xPoint =
            sortedListOfPoints[sortedListOfPoints.length - 1].x + i * 86400;
          console.log(xPoint);
          console.log(data.linear_function.coef * xPoint);
          linearPoints.push({
            x: xPoint,
            y:
              data.linear_function.coef * (xPoint - originTimestamp) +
              data.linear_function.intercept,
          });
        }
        setLinearFunctionPoints(linearPoints);
        // setFilterValues(values);
        setDataLoaded(true);
      })
      .catch((error) => console.log(error));
  }

  useEffect(() => {
    // if (dataLoaded) {
    //   document.getElementsByClassName("class-form")[0].style.justifyContent =
    //     "start";
    // }
    if (firstLoad) {
      handleSubmit({
        values: {
          date: "2023-05-03",
          hour: "23:30:00",
          stationNumber: "194",
        },
      });
      setFirstLoad(false);
    }
  }, [dataLoaded]);

  return (
    <div className="flex h-screen w-screen flex-col items-center justify-center bg-slate-200 bg-opacity-80 bg-[radial-gradient(#444cf7_0.5px,_transparent_0.5px),_radial-gradient(#444cf7_0.5px,_#e5e5f7_0.5px)] bg-[length:20px_20px]">
      {!dataLoaded ? (
        <CompassLoader />
      ) : (
        <Plot
          data={[
            {
              x: points.map((point) => new Date(point.x)),
              y: points.map((point) => point.y),
              type: "scatter",
              mode: "lines+markers",
              marker: { color: "blue" },
            },
            {
              x: linearFunctionPoints.map((point) => new Date(point.x)),
              y: linearFunctionPoints.map((point) => point.y),
              type: "scatter",
              mode: "lines+markers",
              marker: { color: "red" },
            },
          ]}
          layout={{
            width: 1000,
            height: 800,
            title: "Predicción con regresión",
            yaxis: {
              range: yLimits,
            },
          }}
        />
      )}
    </div>
  );
}
