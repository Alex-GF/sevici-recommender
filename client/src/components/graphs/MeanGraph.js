import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import CompassLoader from "../compassLoader";
import { API_SERVER } from "../../settings";

export default function MeanGraph({
  date,
  hour,
  stationNumber,
  width,
  height,
}) {
  let [points, setPoints] = useState([]);
  let [predictionPoint, setPredictionPoint] = useState({});
  let [dataLoaded, setDataLoaded] = useState(false);
  let [yLimits, setYLimits] = useState([0, 50]);

  function handleSubmit({ values }) {
    setDataLoaded(false);

    let query = `${API_SERVER}predictors/mean?`;

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
        let sortedListOfPoints = data.evolution.sort((a, b) => a.x - b.x);
        let maxY = Math.max(...sortedListOfPoints.map((point) => point.y)) + 5;
        let minY = Math.min(...sortedListOfPoints.map((point) => point.y)) - 5;

        setYLimits([minY, maxY]);

        setPoints(sortedListOfPoints);

        let originTimestamp = sortedListOfPoints[0].x;

        setPredictionPoint({
          x: data.prediction[0],
          y: data.prediction[1],
        });

        setDataLoaded(true);
      })
      .catch((error) => console.log(error));
  }

  useEffect(() => {

    if (!dataLoaded) {
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
              x: [new Date(parseInt(predictionPoint.x)*1000)],
              y: [predictionPoint.y],
              type: "scatter",
              mode: "lines+markers",
              marker: { color: "green" },
              name: "Predicción",
            },
          ]}
          layout={{
            width: width,
            height: height,
            title: "Predicción con media",
            yaxis: {
              range: yLimits,
            },
          }}
        />
      )}
    </>
  );
}
