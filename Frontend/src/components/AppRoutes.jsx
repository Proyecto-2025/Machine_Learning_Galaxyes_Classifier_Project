import { Routes,Route, Router } from 'react-router-dom'
import Header from "./Header";
import Predict from './Predict.jsx'
import About from './About.jsx'
import Home from './Home.jsx'
import Learn from './Learn.jsx'
export default function AppRoutes() {
    return (
        <>
            <Header />
            <div className='routes-container'>
                <Routes>    
                    <Route path="/" element={<Home />} />
                    <Route path="/predict" element={<Predict />} />
                    <Route path="/about" element={<About />} />
                    <Route path="/learn" element={<Learn />} />
                </Routes>
            </div>
        </>
    );
}
