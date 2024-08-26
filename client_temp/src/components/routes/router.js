import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './home'


const RouterComponent = () => {
    return (
                <div>

                    <Routes>
                        <Route path="/" element={<Home />} />
                        {/* <Route path="/api/paypal/success" element={<Home/>} />
                <Route path="/api/paypal/cancel" element={<Home {...props} />} />
                <Route path="/api/crypto/success" element={<Home {...props} />} />
                <Route path="/api/crypto/cancel" element={<Home {...props} />} />
                <Route path="*" element={<NoMatch {...props} />} /> */}
                    </Routes>
                </div>
    )
}

export default RouterComponent