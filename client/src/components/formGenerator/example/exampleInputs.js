import { exampleValidators } from "./exampleValidators";

export const exampleInputs = [
    {
      tag: 'Campo de texto',
      name: 'text-field',
      type: 'text',
      defaultValue: "",
      isRequired: true,
      validators: [
        exampleValidators.notEmptyValidator,
      ]
    },
    {
        tag: "Campo de contraseña",
        name: "password-field",
        type: "password",
        defaultValue: "",
        isRequired: true,
        validators: [
            exampleValidators.notEmptyValidator,
            exampleValidators.passwordLengthValidator
        ]
    },
    {
        tag: "Campo de email",
        name: "email-field",
        type: "email",
        defaultValue: "",
        isRequired: true,
        validators: [
            exampleValidators.notEmptyValidator,
            exampleValidators.emailValidator
        ]
    },
    {
      tag: 'Campo numérico',
      name: 'number-field',
      type: 'number',
      defaultValue: "5",
      isRequired: false,
      validators: [
        exampleValidators.minNumber,
        exampleValidators.maxNumber
      ]
    },
    {
      tag: 'Campo de selección',
      name: 'select-field',
      type: 'select',
      values: ["Opción 1", "Opción 2", "Opción 3"],
      defaultValue: "",
      isRequired: true,
      validators: [
        exampleValidators.validOption,
        exampleValidators.notEmptyValidator
      ]
    },
    {
      tag: 'Campo de texto plano',
      name: 'textarea-field',
      type: 'textarea',
      defaultValue: "Esta es una descripción de ejemplo",
      isRequired: true,
      validators: [

      ] 
    },
    {
      tag: 'Campo de imágenes y archivos',
      name: 'files-field',
      type: 'files',
      defaultValue: "",
      isRequired: false,
      validators: []
    },
    {
        tag: "Campo de intervalo",
        name: "interval-field",
        type: "interval",
        min: 0,
        max: 2000,
        defaultValue: "",
        isRequired: true,
        validators: []
    },
    {
        tag: "Campo de fecha",
        name: "date-field",
        type: "date",
        defaultValue: "2023-03-01",
        isRequired: false,
        validators: []
    }
]