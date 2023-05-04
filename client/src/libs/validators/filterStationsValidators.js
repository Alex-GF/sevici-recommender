export const filterStationsValidators = {

    validStatus: {
        validate: (value) => {
            let validStatus = ['Abierta', 'Cerrada', 'Cualquiera'];
            return validStatus.includes(value);
        },
        message: "El campo debe ser un estado válido",
    },
    validMethod: {
        validate: (value) => {
            let validStatus = ['Media', 'Regresión'];
            return validStatus.includes(value);
        },
        message: "El campo debe ser un método válido",
    },
    notFutureDate: {
        validate: (value) => {
            return new Date(value) < new Date();
        },
        message: "La fecha no puede ser posterior a la actual"
    },
    notNegativeNumber: {
        validate: (value) => {
            return value >= 0;
        },
        message: "El campo no puede ser un número negativo"
    },
    notNegativeOrZeroNumber: {
        validate: (value) => {
            return value > 0;
        },
        message: "El campo debe ser mayor que 0"
    }

}