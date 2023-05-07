import { filterStationsValidators } from '../libs/validators/filterStationsValidators';
import moment from 'moment';

export const predictStationsInputs = [
    {
      tag: 'Número de estación',
      name: 'stationNumber',
      type: 'number',
      defaultValue: "",
      isRequired: true,
      validators: [filterStationsValidators.notNegativeNumber, filterStationsValidators.notEmptyValidator]
    },
    {
      tag: "Fecha",
      name: "date",
      type: "date",
      defaultValue: moment().format('YYYY-MM-DD'),
      isRequired: true,
      validators: [filterStationsValidators.notPastDate, filterStationsValidators.notMoreThanOneWeek, filterStationsValidators.notEmptyValidator]
    },
    {
      tag: "Hora",
      name: "hour",
      type: "time",
      defaultValue: "23:59",
      isRequired: true,
      validators: [filterStationsValidators.notEmptyValidator]
    }
]