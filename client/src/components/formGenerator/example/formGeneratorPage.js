import FormGenerator from "../formGenerator";
import { exampleInputs } from "./exampleInputs";
import { useRef } from "react";

const FormGeneratorPage = () => {

    const formRef = useRef(null);

    function handleFormSubmit({values}) {

        if(!formRef.current.validate()) {
            alert ("El formulario no es válido")
            return; // This will validate the form and won't submit if it's not valid
        }

        let exampleValues = "";

        for(let key in values) {
            exampleValues += `${key}: ${values[key]}\n`;
        }

        alert(exampleValues);
    }


    return(
        <div className="bg-[radial-gradient(#444cf7_0.5px,_transparent_0.5px),_radial-gradient(#444cf7_0.5px,_#e5e5f7_0.5px)] flex h-screen w-screen flex-col items-center justify-center bg-slate-200 bg-opacity-80 bg-[length:20px_20px]">

        <div className="max-h-[1000px] max-w-xl h-[90%] w-[90%] rounded-md bg-white flex flex-col justify-evenly items-center p-8">
            <FormGenerator
                ref={formRef}
                inputs={exampleInputs}
                onSubmit={handleFormSubmit}
                numberOfColumns={1} // Can be changed to try with more columns
                scrollable
                listenEnterKey // Remove this prop to disable the enter key listener
                buttonText="Finalizar"
                buttonClassName="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
                {/* If necesary, you can put your own inputs as childs of the generator, and specify where they must be rendered by using 'childrenPosition' prop */}
            </FormGenerator>
        </div>

        </div>
    );
}

export default FormGeneratorPage;