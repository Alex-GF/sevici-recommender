export const filterStationsValidators = {

    validStatus: {
        validate: (value) => {
            let validStatus = ['Abierta', 'Cerrada', 'Cualquiera'];
            return validStatus.includes(value);
        },
        message: "El campo debe ser un estado válido",
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
    notPastDate: {
        validate: (value) => {
            return new Date(value) >= new Date();
        },
        message: "La fecha no puede ser anterior a la actual"
    }, 
    notMoreThanOneWeek: {
        validate: (value) => {
            return new Date(value) < new Date(new Date().getTime() + 7 * 24 * 60 * 60 * 1000);
        },
        message: "La fecha no puede ser posterior a una semana"
    },
    positiveNumber: {
        validate: (value) => {
            return value > 0;
        },
        message: "El campo debe ser un número positivo"
    }
}