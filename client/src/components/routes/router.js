import React, { useState } from "react";
import { Routes, Route } from 'react-router-dom'
import Home from './home'
import Roulette from '../../games/roulette'
import BlackJack from '../../games/blackjack'

const RouterComponent = () => {
    const [connect, setConnect] = useState(false);
    const handleSetConnect = (newTarget) => {
        setConnect(newTarget);
        console.log(connect);
    };


    return (
                <div>
                    <Routes>
                        <Route path="/" element={<Home onSetConnect={handleSetConnect}/>} />
                        <Route path="/roulette" element={<Roulette />} />
                        <Route path="/blackjack" element={<BlackJack /> } />
                    </Routes>
                </div>
    )
}

export default RouterComponent