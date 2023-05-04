import { filterStationsValidators } from '../libs/validators/filterStationsValidators';
import moment from 'moment';

export const filterStationsInputs = [
    {
      tag: 'Número de estación',
      name: 'stationNumber',
      type: 'number',
      defaultValue: "",
      isRequired: false,
      validators: [filterStationsValidators.positiveNumber]
    },
    {
      tag: 'Bicis disponibles',
      name: 'availableBikes',
      type: 'number',
      defaultValue: "",
      isRequired: false,
      validators: [filterStationsValidators.notNegativeNumber]
    },
    {
      tag: 'Capacidad de la estación',
      name: 'stationCapacity',
      type: 'number',
      defaultValue: "",
      isRequired: false,
      validators: [filterStationsValidators.notNegativeNumber]
    },
    {
      tag: 'Estado',
      name: 'stationStatus',
      type: 'select',
      values: ["Cualquiera", "Abierta", "Cerrada"],
      defaultValue: "Cualquiera",
      isRequired: false,
      validators: [filterStationsValidators.validStatus]
    },
    {
      tag: "Fecha",
      name: "date",
      type: "date",
      defaultValue: moment().format('YYYY-MM-DD'),
      isRequired: false,
      validators: [filterStationsValidators.notFutureDate]
    },
    {
      tag: "Hora",
      name: "hour",
      type: "time",
      defaultValue: "12:00",
      isRequired: false,
      validators: []
    }
]