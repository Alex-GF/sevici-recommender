export const exampleValidators = {
    minNumber: {
        validate: (value) => parseInt(value)>0,
        message: "El valor debe ser mayor de 0"
    },

    maxNumber: {
        validate: (value) => parseInt(value)<500000,
        message: "El valor debe ser menor de 500k"
    },

    notEmptyValidator: {
        validate: (value) => value.trim().length > 0,
        message: "El campo no puede estar vacío"
    },
    
    passwordLengthValidator: {
        validate: (value) => value.trim().length >= 6,
        message: "El campo debe tener al menos 6 caracteres"
    },
    
    emailValidator: {
        validate: (value) => value.match(/^([\w.%+-]+)@([\w-]+\.)+([\w]{2,})$/i),
        message: "El campo debe ser un email válido"
    },
    
    validOption: {
        validate: (value) => {
            let validOptions = ['Opción 1', 'Opción 2', 'Opción 3'];
            return validOptions.includes(value);
        },
        message: "El campo debe ser una opción válida",
    },
}