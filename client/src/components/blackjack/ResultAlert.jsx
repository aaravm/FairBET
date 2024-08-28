import React from 'react';

const ResultAlert = (props) => {
    return (
        <div>
            {props.Result ?<div className='result'>
                    <span>{props.Result}</span>
                </div>
                :null}
        </div>
    );
};

export default ResultAlert;