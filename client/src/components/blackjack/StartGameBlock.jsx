import React from 'react';

const StartGameBlock = (props) => {
    return (
        <React.Fragment>
            <div onClick={()=>props.Player_step(props.Counter)} className="yes">
                <span>Еще</span>
            </div>
            <div className="player">
                <span>Player</span>
                    <br/>
                <span style={{color: props.Colors}}>{props.Scor}</span>
            </div>
            <div onClick={props.Pass} className="pass">
                <span >Pass</span>
            </div>
            {props.Scor >= 21 || props.BotSop ?
                <div onClick={props.Continue} className='continue'>
                    <span >New Bid</span>
                </div>
                : null}
        </React.Fragment>
    );
};

export default StartGameBlock;