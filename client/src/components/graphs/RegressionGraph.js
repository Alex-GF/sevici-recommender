import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import CompassLoader from "../compassLoader";

export default function RegressionGraph({date, hour, stationNumber, width, height}) {
  let [points, setPoints] = useState([]);
  let [linearFunctionPoints, setLinearFunctionPoints] = useState([]);
  let [dataLoaded, setDataLoaded] = useState(false);
  let [yLimits, setYLimits] = useState([0, 50]);
  let [prediction, setPrediction] = useState({});

  function handleSubmit({ values }) {

    let query = "http://localhost:8000/api/station?";

    for (let key in values) {
      if (values[key]) {
        if(key === "hour"){
          query += `${key}=${values[key]}:00&`;
        }else{
          query += `${key}=${values[key]}&`;
        }
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
        setPrediction({
          x: parseInt(data.prediction.x)*1000,
          y: data.prediction.y <= 0 ? 0 : data.prediction.y,
        });

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
        
        for (let i = 1; i <= 7; i++) {
          let xPoint =
            sortedListOfPoints[sortedListOfPoints.length - 1].x + i * 86400;
          
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
    if(!dataLoaded){
      handleSubmit({
        values: {
          date: date,
          hour: hour,
          stationNumber: stationNumber,
        },
      }); 
    }
  }, [dataLoaded]);

  useEffect(() => {
    setDataLoaded(false);
  }, [stationNumber, date, hour]);

  return (
    <>
      {!dataLoaded ? (
        <CompassLoader />
      ) : (
        <Plot
          data={[
            {
              x: points.map((point) => new Date(parseInt(point.x)*1000)),
              y: points.map((point) => point.y),
              type: "scatter",
              mode: "lines+markers",
              marker: { color: "blue" },
              name: "Datos previos estación",
            },
            {
              x: linearFunctionPoints.map((point) => new Date(parseInt(point.x)*1000)),
              y: linearFunctionPoints.map((point) => point.y),
              type: "scatter",
              mode: "lines+markers",
              marker: { color: "red" },
              name: "Tendencia predicciones",
            },
            {
              x: [new Date(prediction.x)],
              y: [prediction.y],
              type: "scatter",
              mode: "lines+markers",
              marker: { color: "green" },
              name: "Predicción",
            },
          ]}
          layout={{
            width: width,
            height: height,
            title: "Predicción con regresión",
            yaxis: {
              range: yLimits,
            },
          }}
        />
      )}
    </>
  );
}
