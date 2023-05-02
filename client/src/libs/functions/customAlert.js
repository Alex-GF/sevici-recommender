import { useEffect, useRef } from "react";

import CustomModal from "../../components/customModal";
import ReactDOM from "react-dom/client";

const alert = ReactDOM.createRoot(document.getElementById("alert"));

function customAlert(string) {
  
    const Alert = () => {
      const alertRef = useRef(null);

      useEffect(() => {
        alertRef.current.open();
      }, []);

      return (
        <CustomModal maxHeight={250} ref={alertRef} border={"2px solid black"}>
          <h3 style={{ textAlign: "center" }}>{string}</h3>
        </CustomModal>
      );
    };

    alert.render(<Alert />);
}

export default customAlert;
