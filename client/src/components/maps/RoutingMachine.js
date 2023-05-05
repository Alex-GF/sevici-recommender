import L from "leaflet";
import { createControlComponent } from "@react-leaflet/core";
import "leaflet-routing-machine";

const createRoutineMachineLayer = (props) => {

  const { origin, destination, setTime, setTotalDistance } = props;

  const originIcon = L.icon({
    iconUrl:
      '/location-red.png',
      iconSize: [30, 30],
  });

  const destinationIcon = L.icon({
    iconUrl:
      '/location-blue.png',
    iconSize: [30, 30],
  });

  const instance = L.Routing.control({
    waypoints: [
      L.latLng(origin.lat, origin.lng),
      L.latLng(destination.lat, destination.lng)
    ],
    lineOptions: {
      styles: [{ color: "#6FA1EC", weight: 4 }]
    },
    alternativeClassName: "hidden",
    plan: L.Routing.plan(
      [
        L.latLng(origin.lat, origin.lng),
        L.latLng(destination.lat, destination.lng),
      ],
      {
        createMarker: function (i, wp, nWps) {
          if (i === 0) {
            return L.marker(wp.latLng, { icon: originIcon, });
          }
          return L.marker(wp.latLng, { icon: destinationIcon });
        },
      }
    ),
  });

  return instance;
};

const RoutingMachine = createControlComponent(createRoutineMachineLayer);

export default RoutingMachine;