import { filterStationsValidators } from '../libs/validators/filterStationsValidators';
import moment from 'moment';

export const bestStationPredictorInputs = [
    {
      tag: 'Mínimo de bicis disponibles',
      name: 'availableBikes',
      type: 'number',
      defaultValue: "",
      isRequired: true,
      validators: [filterStationsValidators.notNegativeNumber, filterStationsValidators.notEmptyValidator]
    },
    {
      tag: 'Radio de búsqueda (km)',
      name: 'radius',
      type: 'number',
      defaultValue: "5",
      isRequired: true,
      validators: [filterStationsValidators.notNegativeNumber, filterStationsValidators.notEmptyValidator]
    },
    {
      tag: 'Método de predicción',
      name: 'select',
      values: ["Media", "Regresión"],
      type: 'select',
      defaultValue: "",
      isRequired: true,
      validators: [filterStationsValidators.validMethod, filterStationsValidators.notEmptyValidator]
    },
    {
      tag: "Fecha",
      name: "date",
      type: "date",
      defaultValue: moment().format('YYYY-MM-DD'),
      isRequired: true,
      validators: [filterStationsValidators.notEmptyValidator]
    },
    {
      tag: "Hora",
      name: "hour",
      type: "time",
      defaultValue: "23:59",
      isRequired: true,
      validators: [filterStationsValidators.notEmptyValidator]
    },
    {
      tag: 'Límite de estaciones a mostrar',
      name: 'limit',
      type: 'number',
      defaultValue: "1",
      isRequired: true,
      validators: [filterStationsValidators.notNegativeOrZeroNumber, filterStationsValidators.notEmptyValidator]
    },
]