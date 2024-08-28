import React from 'react';

const BlockCarts = (props) => {
    return (
        <div className="block_carts">
            <img src={props.BG} alt="none" className="cart_bg"/>

            {props.Carts.map((el, index) => {
                const pos = 440
                let pos2 = 28 - (props.Count_pl * 5.7)
                if (props.Count_pl == 2) {

                    pos2 = 17
                }
                return (
                    <img
                        key={index}
                        src={el.src}
                        alt="none"
                        id={`a${index}`}
                        style={index >= 2 && el.st === 'player' ? {transform: `translate(${22.5}vw, ${200}px`} : null
                        || index >= 3 && el.st === 'bot' ? {transform: `translate(${pos2}vw, ${-50}px`} : null}
                        className={el.st === 'player' ? "cart move" : "cart" && el.st === 'bot' ? 'cart bot' : 'cart'}
                    />
                )
            })}
        </div>
    );
};

export default BlockCarts;