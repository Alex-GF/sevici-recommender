export const filterStationsValidators = {

    validStatus: {
        validate: (value) => {
            let validStatus = ['Abierta', 'Cerrada', 'Cualquiera'];
            return !value || validStatus.includes(value);
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
            return !value || new Date(value) < new Date();
        },
        message: "La fecha no puede ser posterior a la actual"
    },
    notNegativeNumber: {
        validate: (value) => {
            return !value || value >= 0;
        },
        message: "El campo no puede ser un número negativo"
    },
    notNegativeOrZeroNumber: {
        validate: (value) => {
            return value > 0;
        },
        message: "El campo debe ser mayor que 0"
    
    },
    notPastDate: {
        validate: (value) => {
            return !value || new Date(value) >= new Date();
        },
        message: "La fecha no puede ser anterior a la actual"
    }, 
    notMoreThanOneWeek: {
        validate: (value) => {
            return !value || new Date(value) < new Date(new Date().getTime() + 7 * 24 * 60 * 60 * 1000);
        },
        message: "La fecha no puede ser posterior a una semana"
    },
    positiveNumber: {
        validate: (value) => {
            return !value || value > 0;
        },
        message: "El campo debe ser un número positivo"
    },
    notEmptyValidator: {
        validate: (value) => {
            return value.trim().length > 0;
        },
        message: "El campo no puede estar vacío"
    }
}