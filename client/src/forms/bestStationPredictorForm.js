import { filterStationsValidators } from '../libs/validators/filterStationsValidators';
import moment from 'moment';

export const bestStationPredictorInputs = [
    {
      tag: 'Mínimo de bicis disponibles',
      name: 'minBikes',
      type: 'number',
      defaultValue: "",
      isRequired: true,
      validators: [filterStationsValidators.notNegativeNumber]
    },
    {
      tag: 'Radio de búsqueda (km)',
      name: 'radius',
      type: 'number',
      defaultValue: "5",
      isRequired: true,
      validators: [filterStationsValidators.notNegativeNumber]
    },
    {
      tag: 'Método de predicción',
      name: 'select',
      values: ["Media", "Regresión"],
      type: 'select',
      defaultValue: "",
      isRequired: true,
      validators: [filterStationsValidators.validMethod]
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
    },
    {
      tag: 'Límite de estaciones a mostrar',
      name: 'limit',
      type: 'number',
      defaultValue: "1",
      isRequired: true,
      validators: [filterStationsValidators.notNegativeOrZeroNumber]
    },
]