import React from 'react';
import { FaTimes } from 'react-icons/fa'; // Font Awesome Close Icon
import './../../games/roulette.css';

const ResultAlert = (props) => {
    const handleClose = () => {
        props.setResult(''); // Set the result to an empty string
    };

    return (
        <div>
            {props.Loading && (
                <>
                {/* Backdrop to darken background */}
                <div className="backdrop"></div>

                {/* Pop-up result */}
                <div className={`loading`}>
                    <span>Securely computing on Nillion!!</span>
                </div>
            </>
            )}
            {props.Result && (
                <>
                    {/* Backdrop to darken background */}
                    <div className="backdrop"></div>

                    {/* Close button in the top-right of the viewport */}
                    <FaTimes className="close-icon" onClick={handleClose} />

                    {/* Pop-up result */}
                    <div className={`result ${props.Result === 'True' ? 'victory' : 'lost'}`}>
                        <span>{props.Result === 'True' ? 'Victory' : 'Lost'}</span>
                    </div>
                </>
            )}
        </div>
    );
};

export default ResultAlert;
