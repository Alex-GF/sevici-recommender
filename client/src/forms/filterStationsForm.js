import { filterStationsValidators } from '../libs/validators/filterStationsValidators';
import moment from 'moment';

export const filterStationsInputs = [
    {
      tag: 'Bicis disponibles',
      name: 'available-bikes',
      type: 'number',
      defaultValue: "",
      isRequired: false,
      validators: [filterStationsValidators.notNegativeNumber]
    },
    {
      tag: 'Capacidad de la estación',
      name: 'station-capacity',
      type: 'number',
      defaultValue: "",
      isRequired: false,
      validators: [filterStationsValidators.notNegativeNumber]
    },
    {
      tag: 'Estado',
      name: 'station-status',
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
      name: "time",
      type: "time",
      defaultValue: "12:00",
      isRequired: false,
      validators: []
    }
]