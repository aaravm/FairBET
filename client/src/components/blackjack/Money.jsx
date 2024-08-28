import React from 'react';

const Money = (props) => {
    return (
        <div className='money'>
            <div>
                <span className='money_title'>Manager Cards : {props.Score_bot} </span>
            </div>
            <div >
                <span className='money_title'>Money : {props.Money} $</span>
                <span className='money_title'>Bid : {props.Input} $</span>
            </div>
        </div>
    );
};

export default Money;