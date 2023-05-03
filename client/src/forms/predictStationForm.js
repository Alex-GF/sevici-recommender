import { filterStationsValidators } from '../libs/validators/filterStationsValidators';
import moment from 'moment';

export const predictStationsInputs = [
    {
      tag: 'Número de estación',
      name: 'stationNumber',
      type: 'number',
      defaultValue: "",
      isRequired: true,
      validators: [filterStationsValidators.notNegativeNumber]
    },
    {
      tag: "Fecha",
      name: "date",
      type: "date",
      defaultValue: moment().format('YYYY-MM-DD'),
      isRequired: true,
      validators: []
    },
    {
      tag: "Hora",
      name: "hour",
      type: "time",
      defaultValue: "23:59",
      isRequired: true,
      validators: []
    }
]