import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './home'
import Roulette from '../../games/roulette'
import BlackJack from '../../games/blackjack'
import Auth from '../auth/Auth'

const RouterComponent = () => {
    return (
                <div>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/roulette" element={<Roulette />} />
                        <Route path="/blackjack" element={<BlackJack /> } />
                        <Route path="/auth" element={<Auth/> } />
                    </Routes>
                </div>
    )
}

export default RouterComponent