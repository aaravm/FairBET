import React, { useState } from "react";
import { Routes, Route } from 'react-router-dom'
import Home from './home'
import Roulette from '../../games/roulette'
import BlackJack from '../../games/blackjack'
import { useStateContext } from "../../context";

const RouterComponent = () => {
    const { account } = useStateContext();

    return (
                <div>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/roulette" element={<Roulette />} />
                        <Route path="/blackjack" element={<BlackJack /> } />
                    </Routes>
                </div>
    )
}

export default RouterComponent