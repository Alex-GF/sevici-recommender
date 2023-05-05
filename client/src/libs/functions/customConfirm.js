import "../../static/css/confirm.css";

import { useRef, useEffect } from "react";

import ReactDOM from 'react-dom/client';
import CustomModal from "../../components/customModal";

const confirm = ReactDOM.createRoot(document.getElementById('confirm'));

function customConfirm(string) {

    return new Promise(function(resolve, reject) {

        const Confirm = () => {
    
            const confirmModalRef = useRef(null);
    
            const confirmClick = () => {
                confirmModalRef.current.close();
                resolve();
            }
    
            const denyClick = () => {
                confirmModalRef.current.close();
                reject();
            }

            useEffect(() => {
                confirmModalRef.current.open();
            }, []);
    
            return (
                <CustomModal
                    ref={confirmModalRef}
                    maxHeight={250}
                    maxWidth={500}
                    border={"2px solid black"}
                >
                    <h3 className="class-confirm-text">{string}</h3>
                    <div className="class-buttons-line d-flex justify-content-between w-100">
                        <div className="class-confirm-btn" onClick={denyClick}>Denegar</div>
                        <div className="class-confirm-btn" onClick={confirmClick}>Confirmar</div>
                    </div>   
                </CustomModal>
            );
        }
    
        confirm.render(<Confirm/>);
    })
}

export default customConfirm;