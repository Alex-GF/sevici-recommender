export const filterStationsInputs = [
    {
      tag: 'Bicis disponibles',
      name: 'available-bikes',
      type: 'number',
      defaultValue: "1",
      isRequired: false,
      validators: []
    },
    {
      tag: 'Capacidad de la estación',
      name: 'station-capacity',
      type: 'number',
      defaultValue: "1",
      isRequired: false,
      validators: []
    },
    {
      tag: 'Estado',
      name: 'station-status',
      type: 'select',
      values: ["Cualquiera", "Abierta", "Cerrada"],
      defaultValue: "Cualquiera",
      isRequired: false,
      validators: []
    },
    {
        tag: "Fecha",
        name: "date",
        type: "date",
        defaultValue: "2023-03-01",
        isRequired: false,
        validators: []
    },
    {
        tag: "Hora",
        name: "time",
        type: "time",
        defaultValue: "20:00",
        isRequired: false,
        validators: []
    }
]