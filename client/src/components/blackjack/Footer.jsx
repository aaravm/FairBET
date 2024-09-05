import React from 'react';
import StartGameBlock from "./StartGameBlock";


const Footer = (props) => {
    return (
        <div className="footer">
            {!props.is_start && <div className='start_block'>
                    <span onClick={() => {
                        props.Money>0?props.Start(props.Carts):props.Restart()
                    }} className='start'>{props.Money>0?'Start':'Hit раз'}</span>
                <div>
                    {props.Money>0?<input className='input' style={props.Money<props.Input?{color:'#FF4848'}:null} onChange={props.OnChange} value={props.Input} type="text"/>:null}
                </div>
            </div>
            }

            {props.is_start &&
            <StartGameBlock
                Counter={props.Counter}
                OnChange={props.OnChange}
                BotSop={props.BotStop}
                Input={props.Input}
                Continue={props.Continue}
                Pass={props.Pass}
                Player_step={props.Player_step}
                Scor={props.Scor}
                Colors={props.Colors}/>
            }
        </div>
    );
};

export default Footer;