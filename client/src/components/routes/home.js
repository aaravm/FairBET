import React from "react";
import Connect  from "../connect";
import "./home.css"
import roulette from "./../../images//roulette-icon.png";
import blackjack from "./../../images//blackjack-icon.png";
import { useStateContext } from "../../context";
import { useNavigate } from "react-router-dom";

const Home = () => {
    const { account } = useStateContext();
    const navigate = useNavigate();


    const handleRoulette = () => {
        if(!(account === '')){
            navigate('/roulette');
        }
    }

    const handleBlackjack = () => {
        if (!(account === '')) {
            navigate('/blackjack');
        }
    }

    return (
        <div className="home">
            <div className="top">
                <div className="navbar">
                    <div className="navbar-content">
                        <h1 className="title">FairBET</h1>
                        <Connect />
                    </div>
                </div>
            </div>
            <div className="selector">
                <div className="content" onClick={handleRoulette}>
                    <img src={roulette} height={300} alt="roullete img"/>
                    <h1>Roulette</h1>
                </div>
                <div className="content" onClick={handleBlackjack}>
                    <img src={blackjack} height={300} alt="blackjack img"/>
                    <h1>Blackjack</h1>
                </div>
            </div>
        </div>
    )
}

export default Home