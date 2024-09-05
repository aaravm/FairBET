import React from "react";
import Connect  from "./connect";
import "./home.css"
import roulette from "./../../images//roulette-icon.png";
import blackjack from "./../../images//blackjack-icon.png";


const Home = () => {
    return (
        <div className="home">
            <div className="top">
                <div className="navbar">
                    <div className="navbar-content">
                        <h1 className="title">FairBET</h1>
                        <Connect/>
                    </div>
                </div>
            </div>
            <div className="selector">
                <div className="content">
                    <img src={roulette} height={300}/>
                    <h1>Roulette</h1>
                </div>
                <div className="content">
                    <img src={blackjack} height={300}/>
                    <h1>Blackjack</h1>
                </div>
            </div>
        </div>
    )
}

export default Home